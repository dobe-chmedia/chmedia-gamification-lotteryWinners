##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""a helper class which connects to the funifier API.\n
    
The code has following regions:\n
     - players:\n

     - challenges:\n

     - action:\n

     - action_log:\n

     - lottery:\n

     - levels:\n

source: https://api.funifier.com/
"""
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-02-20          bettlerd    created script
##* 2023-02-24          bettlerd    added get_lottery_participants
##* 2023-03-14          bettlerd    added count_lottery_participants
##* 2023-03-14          bettlerd    added count_lottery_winners
##* 2023-03-14          bettlerd    updated request body of get_lottery_participants
##*                                     - added $ifNull: {}
##*                                     - removed name
##*                                     - added firstname
##*                                     - added lastname
##*                                     - added tos_accepted
##*                                     - added privacy_accepted
##* 2023-04-11          bettlerd    handling of Funifier API Exceptions
##* 2023-04-12          bettlerd    added n_days to some of the methods
##* 2023-04-18          bettlerd    added body encoding utf-8
##* 2023-04-28          bettlerd    added body encoding utf-8
##* 2023-05-02          bettlerd    update __define_time_period() adding coma & attribute
##* 2023-05-02          bettlerd    update get_all_wheel_of_fortunes MongoDB query
##* 2023-06-16          bettlerd    rename profileCreatedDate to openingDateOfPlayerFromFunifier
##* 2023-06-16          bettlerd    added n_days in get_all_players()
##* 2023-06-19          bettlerd    added ifNull handling in get_all_players()
##* 2023-06-26          bettlerd    added get_all_players_in_date_range()
##* 2023-06-29          bettlerd    added timeperiod to get_wheel_of_fortunes_activities()
##* 2023-07-07          bettlerd    added get_all_lottery_in_date_range()
##* 2023-08-09          bettlerd    added get_all_lottery_tickets_in_date_range()
##* 2023-10-05          bettlerd    added StringIO in __get_data() since passing 
##*                                 a string to pd.read_json() is deprecated
##* 2023-10-05          bettlerd    added methods:
##*                                     - get_all_lottery_by_lottery_uids()
##*                                     - get_all_lottery_uids_in_date_range()
##* 2023-10-05          bettlerd    added do_logging(), update doc strings by GitHub Copilot
##* 2023-10-05          bettlerd    added get_all_lottery_uid_by_last_n_entries()
##* 2023-10-25          bettlerd    changed helper to service
##* 2023-10-25          bettlerd    updated get_lottery_participants(), added which_tickets
##* 2023-12-25          bettlerd    added get_lottery_winners_with_address()
##*
##*

import http.client
from io import StringIO
import json
import base64
import logging
from typing import List
import pandas as pd

from common.enums.common.encoding import EncodingEnum
from common.enums.common.http_methods import HTTPmethodsEnum
from common.exceptions.funifier.api_error import FunifierAPIError
from common.helper.logging_helper import do_logging
from domain_objects.dto.funifier.api_response_dto import APIResponseDTO
from domain_objects.dto.common.api_config_dto import APIConfigsDTO
import common.constants.funifier.pattern as pattern
import common.constants.funifier.routes as routes


class FunifierAPI():
    """
    Gives access to the Funifier API

    source: https://api.funifier.com/
    """

    def __init__(self, config:APIConfigsDTO):
        do_logging("Initializing Funifier API")
        self.__API_KEY = config.api_key
        self.__APP_SECRET = config.app_secret
        self.__URL = config.url
        self.__VERSION = config.version
        self.__HEADER = config.header
    
    def __API_request(self, method:str,route:str, body=None):
        conn = http.client.HTTPSConnection(self.__URL) 
        headers = {
          'Content-Type': self.__HEADER.content_type,
          'Authorization': 'Basic {}'.format(
            base64.b64encode(bytes(f'{self.__API_KEY}:{self.__APP_SECRET}',
                                   EncodingEnum.UTF8.value))
                  .decode(EncodingEnum.ASCII.value)),
          'Range': self.__HEADER.range
        }
        
        conn.request(method, f"/{self.__VERSION}{route}",body=body, headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        return data.decode(EncodingEnum.UTF8.value)
    
    def __GET_request(self, route:str):
        return self.__API_request(method=HTTPmethodsEnum.GET.value,
                                  route=route)
    
    def __POST_request(self,route:str,body:str):       
        return self.__API_request(method=HTTPmethodsEnum.POST.value,
                                  route=route,
                                  body=body.encode(EncodingEnum.UTF8.value))

    #region lottery
    def count_lottery_participants(self,ticketUID:str)->int:
        """
        Returns the count of all the participants of the given lottery ticket from the Funifier collection "achievement".

        Args:
            ticketUID (str): The UID of the lottery ticket to count the participants for defined in the excel sheet 
                            «Customer Regional - Gamification» in sheet «Campaigns».

        Returns:
            int: The count of the lottery participants.

        Notes:
            - This method sends a POST request to the Funifier API using the `DB_ACHIEVEMENT_AGGR` route.
            - The request body is a MongoDB aggregation pipeline that matches the achievement data for the given lottery ticket UID and type 2 (lottery ticket purchase).
            - The `$count` stage is used to count the number of unique players who purchased the lottery ticket.
            - The resulting API response is a JSON string containing the count of the lottery participants.
            - The JSON string is transformed into a Pandas DataFrame using the `pd.read_json()` method.
            - The `__get_counts()` method is called to extract the count from the DataFrame.
            - The `do_logging()` function is called to log the start of the method execution.

        source: https://docs.google.com/spreadsheets/d/10Khpsyi3JGwoCZp2z_Y-rhBPXS0fH9-3owuDd18Z7aQ/edit
        """
        # do_logging(f"Getting lottery participants for ticket «{ticketUID}»")
        body = """
            [
                {
                    "$match": {
                        "type": 2,
                        "item": "#ticket_uid#"
                    }
                },
                {
                    "$count": "player"
                },
                {
                    "$project": {
                        "count": "$player"
                    }
                }
            ]      
        """.replace(pattern.TICKET,ticketUID)

        api_res = self.__POST_request(route=routes.DB_ACHIEVEMENT_AGGR,body=body)
        data = pd.read_json(api_res)

        return self.__get_counts(data)

    def get_lottery_winners_with_address(self,lotteryUID:str, ticketUID:str)->pd.DataFrame:
        """
        Returns all the lottery winners of the given lottery from the Funifier collection "achievement".

        Args:
            lotteryUID (str): The UID of the lottery to retrieve the winners for.
            ticketUID (str): The UID of the lottery ticketed corresponding to the lottery UID.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing information about the lottery winners.            
        """
        do_logging(f"Getting lottery winners for lottery «{lotteryUID}»")

        body = (
            """
                [
                    {
                        "$match": {
                        "type": 5,
                        "item": "#lottery_uid#"
                        }
                    },
                    {
                        "$lookup": {
                        "from": "achievement",
                        "let": {
                            "playerUID": "$player"
                        },
                        "pipeline": [
                            {
                            "$match": {
                                "$expr": {
                                "$and": [
                                    { "$eq": ["$type", 2] },
                                    { "$eq": ["$item", "#ticket_uid#"] },
                                    { "$eq": ["$player", "$$playerUID"] }
                                ]
                                }
                            }
                            },
                            {
                            "$group": {
                                "_id": {
                                    "playerUID": "$player",
                                    "firstName": "$extra.firstName",
                                    "lastName": "$extra.lastName",
                                    "phone": "$extra.phone",
                                    "dateOfBirth": "$extra.dateOfBirth",
                                    "street": "$extra.street",
                                    "city": "$extra.city",
                                    "zip": "$extra.zip",
                                    "tos_accepted": "$extra.tos_accepted",
                                    "privacy_accepted": "$extra.privacy_accepted"
                                }
                            }
                            }
                        ],
                        "as": "joinedData"
                        }
                    },
                    {
                        "$project": {
                        "player": 1,
                        "total": 1,
                        "lotteryUID": "$item",
                        "time": 1,
                        "ticketUID": "$extra.ticket",
                        "firstname": { "$arrayElemAt": ["$joinedData._id.firstName", 0] },
                        "lastName": { "$arrayElemAt": ["$joinedData._id.lastName", 0] },
                        "phone": { "$arrayElemAt": ["$joinedData._id.phone", 0] },
                        "dateOfBirth": { "$arrayElemAt": ["$joinedData._id.dateOfBirth", 0] },
                        "street": { "$arrayElemAt": ["$joinedData._id.street", 0] },
                        "city": { "$arrayElemAt": ["$joinedData._id.city", 0] },
                        "zip": { "$arrayElemAt": ["$joinedData._id.zip", 0] },
                        "tos_accepted": { "$arrayElemAt": ["$joinedData._id.tos_accepted", 0] },
                        "privacy_accepted": { "$arrayElemAt": ["$joinedData._id.privacy_accepted", 0] }
                        }
                    }
                ]
            """
            .replace(pattern.LOTTERY,lotteryUID)
            .replace(pattern.TICKET,ticketUID)
        )
        
        api_res = self.__POST_request(route=routes.DB_ACHIEVEMENT_AGGR,body=body)
        return self.__get_data(api_res)

    #endregion

    #region helper methods
    def __define_time_range(
            self,
            from_date:str,
            to_date:str,
            time_attribute:str="time"
        ) -> str:
        """
        Generates a date range query dictionary for the match clause in a MongoDB query.

        Args:
            from_date (str): The start date of the range in ISO format (YYYY-MM-DD).
            to_date (str): The end date of the range in ISO format (YYYY-MM-DD).
            time_attribute (str, optional): The name of the time attribute in the Funifier MongoDB. Defaults to "time".

        Returns:
            str: A string representation of a MongoDB query dictionary with the date range.

        Notes:
            - This method generates a query dictionary with the date range using the `$gte` and `$lte` operators.
            - The `from_date` and `to_date` parameters are converted to ISO format and appended with a constant time string.
            - The resulting query dictionary is returned as a string with single quotes replaced by double quotes and the first and last characters removed.
        """
        TIME_CONST = "T00:00:00.000Z"
        query_dict = {
            time_attribute: {
                "$gte": {
                    "$date": f"{from_date}{TIME_CONST}"
                },
                "$lte": {
                    "$date": f"{to_date}{TIME_CONST}"
                }
            }
        }

        ### Data Preprocessing
        # 1. change single quote to double quote (api request needs double quote)
        # 2. delete 1st and last character i.e. start and end curly bracket { }
        return str(query_dict).replace("'",'"')[1:-1]

    def __define_time_period(
            self, 
            n_days:int, 
            time_attribute:str="time",
            with_leading_coma:bool=True
        )->str:
        """
        Defines the time period for which data will be collected in a MongoDB query.

        Args:
            n_days (int): The number of days in the past for which data should be returned.
            time_attribute (str, optional): The name of the time attribute in the Funifier MongoDB. Defaults to "time".
            with_leading_coma (bool, optional): Determines whether a leading comma should be added to the query string. Defaults to True.

        Returns:
            str: A string representation of a MongoDB query dictionary with the time period.

        Notes:
            - This method generates a query dictionary with the time period using the `$gte` operator and the `$date` operator.
            - The `n_days` parameter is used to calculate the start date of the time period in ISO format.
            - The resulting query dictionary is returned as a string with placeholders for the time attribute and the start date.
            - The placeholders are replaced with the actual values of the `time_attribute` and `str_n_days` variables.
            - The `with_leading_coma` parameter is used to determine whether a leading comma should be added to the query string.
        """
        if n_days == None:
            return ""
        else:
            # n_days == 0, means «today» and this needs an additional minus at the end
            # of the string.
            if n_days == 0:
                str_n_days= f"-{n_days}d-"
            else:
                str_n_days= f"-{n_days}d"

            if with_leading_coma:
                str_comma = ","
            else:
                str_comma = ""
            
            __query = """#leading_coma#"#time_attribute#": {"$gte":{"$date":"#n_days#"}}"""
            return (
                __query.replace(pattern.LEADING_COMA, str_comma)
                       .replace(pattern.TIME_ATTRIBUTE,time_attribute)
                       .replace(pattern.N_DAYS,str_n_days)
            )

    def __get_counts(self,data:pd.DataFrame)->int:
        """
        Extracts the count from a Pandas DataFrame and returns 0 if empty.

        Args:
            data (pd.DataFrame): The Pandas DataFrame containing the count.

        Returns:
            int: The count extracted from the DataFrame.

        Notes:
            - This method checks if the DataFrame is not empty using the `len()` function.
            - If the DataFrame is not empty, it extracts the count from the "count" column using the `data["count"]` syntax.
            - The count is returned as an integer using the `int()` function.
            - If the DataFrame is empty, it returns 0.
        """
        if len(data.index) > 0:
            return int(data["count"])
        else:
            return 0

    def __get_data(self, api_result:str)->pd.DataFrame:
        """
        Extracts the data from the result of a Funifier API call and returns it as a Pandas DataFrame.

        Args:
            api_result (str): The result of the Funifier API call as a string.

        Returns:
            pd.DataFrame: The extracted data as a Pandas DataFrame.

        Raises:
            FunifierAPIError: If the API response has an error code other than 200.

        Notes:
            - This method uses the `pd.read_json()` method to read the API result string as a JSON object and convert it to a Pandas DataFrame.
            - If the API result string cannot be read as a JSON object, it is assumed to be an APIResponseDTO object and is parsed accordingly.
            - If the API response has an error code other than 200, a FunifierAPIError is raised with the error message from the API response.
            - If any other exception occurs during the transformation of the Pandas DataFrame, it is logged and re-raised.
        """
        try:
            data = pd.read_json(StringIO(api_result))
            return data
        except ValueError:
            json_str = json.loads(api_result)
            api_dto = APIResponseDTO.from_dict(json_str)

            if api_dto.errorCode != 200:
                raise FunifierAPIError(api_dto.errorMessage)
        except Exception as e:
            logging.exception(f"error while transforming pandas dataframe. «{e}»")
            raise e
    #endregion

    #region unittest
    def test___define_time_period(self, n_days, time_attribute, with_leading_coma):
        if time_attribute is None and with_leading_coma is None:
            return self.__define_time_period(n_days=n_days)
        else:
            return self.__define_time_period(n_days=n_days, time_attribute=time_attribute, with_leading_coma=with_leading_coma)
    #endregion


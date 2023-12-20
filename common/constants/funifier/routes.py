##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""Funifier API Routes"""
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-04-06          bettlerd    created script
##* 2023-04-12          bettlerd    added DB_MYSTERY_BOX_LOG_AGGR
##* 2023-04-18          bettlerd    added DB_VIRTUAL_GOODS_AGGR
##* 2023-04-28          bettlerd    added DB_LOTTERY_TICKETS_AGGR
##*
##*

ACTION = "/action"
ACTION_LOG = "/action/log"
ACTION_LOG_BULK = "/action/log/bulk"
LVL = "/level"
CHALLENGE = "/challenge"
DB_ACTION_AGGR = "/database/action/aggregate"
DB_ACTION_LOG_AGGR = "/database/action_log/aggregate?strict=true"
DB_ACHIEVEMENT_AGGR = "/database/achievement/aggregate?strict=true"
DB_PLAYER_AGGR = "/database/player/aggregate?strict=true"
DB_PLAYER_STATUS = "/player/status"
DB_PLAYER_ATTRIBUTE = "/player/attribute"
DB_MYSTERY_BOX_LOG_AGGR = "/database/mystery_box_log/aggregate?strict=true"
DB_MYSTERY_BOX_AGGR = "/database/mystery_box/aggregate?strict=true"
DB_LOTTERY_AGGR = "/database/lottery/aggregate?strict=true"
DB_LOTTERY_TICKETS_AGGR = "/database/lottery_ticket/aggregate?strict=true"
DB_VIRTUAL_GOODS_AGGR = "/database/catalog_item/aggregate?strict=true"
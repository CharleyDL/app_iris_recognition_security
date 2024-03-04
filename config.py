#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Thursday 05 Oct. 2023
# ==============================================================================
# Configuration file for the connection to DB
# ==============================================================================


def get_db_config() -> dict:
    """
    Returns a dictionary containing database's informations, which are used
    by the following method : mysql.connector.connect()
    """

    config = {
            "host" : "",
            "user" : "",
            "password" : "",
            "auth_plugin" : "mysql_native_password",
            "port" : "",
            "database" : ""
    }

    return config
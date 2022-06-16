#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os

from ethtx import EthTx, EthTxConfig
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from . import frontend, api

app = Flask(__name__)

ethtx_config = EthTxConfig(
    mongo_connection_string=os.getenv("MONGO_CONNECTION_STRING"),
    etherscan_api_key=os.getenv("ETHERSCAN_KEY"),
    web3nodes={
        "boba": dict(hook=os.getenv("BOBA_NODE_URL", ""), poa=True),
    },
    default_chain="boba",
    etherscan_urls={
        "boba": os.getenv("BOBA_ETHERSCAN_URL", ""),
    },
)

ethtx = EthTx.initialize(ethtx_config)

app.wsgi_app = DispatcherMiddleware(
    frontend.create_app(engine=ethtx, settings_override=EthTxConfig),
    {"/api": api.create_app(engine=ethtx, settings_override=EthTxConfig)},
)

# ethtx_ce/ as Source Root
if __name__ == "__main__":
    app.run()

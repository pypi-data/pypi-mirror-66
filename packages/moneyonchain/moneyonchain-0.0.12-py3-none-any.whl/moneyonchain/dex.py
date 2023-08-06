"""
        GNU AFFERO GENERAL PUBLIC LICENSE
           Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN
 @2020
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import os
import logging
from web3 import Web3
from web3.types import BlockIdentifier

from moneyonchain.contract import Contract
from moneyonchain.admin import ProxyAdmin


class MoCDecentralizedExchange(Contract):
    log = logging.getLogger()

    contract_abi = Contract.content_abi_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MoCDecentralizedExchange.abi'))
    contract_bin = Contract.content_bin_file(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'abi_dex/MoCDecentralizedExchange.bin'))

    mode = 'DEX'
    precision = 10 ** 18

    def __init__(self, connection_manager, contract_address=None, contract_abi=None, contract_bin=None):

        if not contract_address:
            # load from connection manager
            network = connection_manager.network
            contract_address = connection_manager.options['networks'][network]['addresses']['dex']

        super().__init__(connection_manager,
                         contract_address=contract_address,
                         contract_abi=contract_abi,
                         contract_bin=contract_bin)

        # finally load the contract
        self.load_contract()

    def implementation(self, block_identifier: BlockIdentifier = 'latest'):
        """Implementation of contract"""

        contract_admin = ProxyAdmin(self.connection_manager)
        contract_address = Web3.toChecksumAddress(self.contract_address)

        return contract_admin.implementation(contract_address, block_identifier=block_identifier)

    def token_pairs(self, block_identifier: BlockIdentifier = 'latest'):
        """ Get the token pairs"""

        result = self.sc.functions.getTokenPairs().call(
            block_identifier=block_identifier)

        return result

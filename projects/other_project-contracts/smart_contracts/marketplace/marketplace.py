from _algopy_testing.op import Global
from algopy import Txn, arc4, UInt64, Asset, gtxn, itxn


class MarketPlace(arc4.ARC4Contract):
    def __init__(self) -> None:
        self.unitary_price: UInt64
        self.asset_id: UInt64

    @arc4.baremethod(allow_actions=["NoOp"], create="require")
    def create_app(self, asset: Asset, unitary_price: UInt64) -> None:
        self.asset_id = asset.id
        self.unitary_price = unitary_price

    @arc4.abimethod
    def set_price(self, unitary_price: UInt64) -> None:
        assert Txn.sender == Global.creator_address
        self.unitary_price = unitary_price

    @arc4.abimethod
    def opt_in_to_asset(self, mbr: gtxn.PaymentTransaction) -> None:
        assert not Global.current_application_address.is_opted_in(Asset(self.asset_id))
        assert mbr.receiver == Global.current_application_address
        assert mbr.amount == Global.min_balance + Global.asset_opt_in_main_balance
        itxn.AssetTransfer(
            xfer_asset=self.asset_id,
            asset_receiver=Global.current_application_address,
            asset_amount=0,
        ).submit()

    @arc4.abimethod
    def buy(self, quantity: UInt64, buy_txn: gtxn.PaymentTransaction) -> None:
        assert buy_txn.sender == Txn.sender
        assert buy_txn.receiver == Global.current_application_address
        assert buy_txn.amount == self.unitary_price * quantity
        # assert buy_txn.sender.is_opted_in(Asset(self.asset_id))
        itxn.AssetTransfer(
            xfer_asset=self.asset_id,
            asset_receiver=buy_txn.sender,
            asset_amount=quantity,
        ).submit()

    @arc4.abimethod(allow_actions=["DeleteApplication"])
    def delete_app(self) -> None:
        assert Txn.sender == Global.creator_address
        itxn.AssetTransfer(
            xfer_asset=self.asset_id,
            asset_receiver=Global.creator_address,
            asset_amount=0,
            asset_close_to=Global.creator_address,
        ).submit()
        itxn.Payment(
            receiver=Global.creator_address,
            amount=0,
            close_remainder_to=Global.creator_address,
        ).submit()

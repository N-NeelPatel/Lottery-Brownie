from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config, accounts
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]  # latest deployed lottery
    starting_tx = lottery.startLottery(
        {"from": account}
    )  # transaction hence provide address
    starting_tx.wait(1)
    print("The lottery is started!!!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    enter_tx = lottery.enter({"from": account, "value": value})
    enter_tx.wait(1)
    print("entering the lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    end_tx = lottery.endLottery({"from": account})
    end_tx.wait(1)
    time.sleep(180)
    print("Ending the lottery")
    print(f"Winner is {lottery.recentWinner()}")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
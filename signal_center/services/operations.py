import telegram

from django.conf import settings
from signal_center.excepions import LeverageException, VolumeException, BadStopLossException, BadTakeProfitException
from signal_center.models import NewSignal
from accounts.models import ExchangeAccounts


def check_conditions(instance: NewSignal):
    if instance.leverage >= 50:
        raise LeverageException("not allowed leverage more than 50 decrease your leverage")
    if instance.volume <= 40:
        raise VolumeException('minimum volume is 40 $')
    if not instance.is_market:
        if instance.side == NewSignal.LONG:
            if instance.stop_loss > instance.entry_point:
                raise BadStopLossException('stop loss must lower than entry point in Long side')
            if instance.entry_point < instance.tp1 or instance.entry_point < instance.tp2 or \
                    instance.entry_point < instance.tp3 or instance.entry_point < instance.tp4 \
                    or instance.entry_point < instance.tp5:
                raise BadTakeProfitException("take profits must higher than entry point")
            if instance.tp1 > instance.tp2:
                raise BadTakeProfitException("tp1 must be lower than tp2 in LONG")
            if instance.tp2 > instance.tp3:
                raise BadTakeProfitException("tp2 must be lower than tp3 in LONG")
            if instance.tp3 > instance.tp4:
                raise BadTakeProfitException("tp3 must be lower than tp4 in LONG")
            if instance.tp4 > instance.tp5:
                raise BadTakeProfitException("tp4 must be lower than tp5 in LONG")
        elif instance.side == NewSignal.SHORT:
            if instance.stop_loss < instance.entry_point:
                raise BadStopLossException('stop loss must higher than entry point in SHORT side')
            if instance.entry_point > instance.tp1 or instance.entry_point > instance.tp2 or \
                    instance.entry_point > instance.tp3 or instance.entry_point > instance.tp4 \
                    or instance.entry_point > instance.tp5:
                raise BadTakeProfitException("take profits must lower than entry point in SHORT side")
            if instance.tp1 < instance.tp2:
                raise BadTakeProfitException("tp1 must be lower than tp2 in SHORT")
            if instance.tp2 < instance.tp3:
                raise BadTakeProfitException("tp2 must be lower than tp3 in SHORT")
            if instance.tp3 < instance.tp4:
                raise BadTakeProfitException("tp3 must be lower than tp4 in SHORT")
            if instance.tp4 < instance.tp5:
                raise BadTakeProfitException("tp4 must be lower than tp5 in SHORT")


class TelegramManager:

    @classmethod
    def send(cls, message: str) -> None:
        # create a bot telegram instance with settings
        pp = telegram.utils.request.Request(proxy_url=settings.TELEGRAM_URL_PROXY)
        bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN, request=pp)

        try:
            bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message, parse_mode=None, timeout=float(5))
        except Exception as e:
            raise


class MessageTemplator:

    @staticmethod
    def get_new_signal_message(instance: NewSignal) -> str:
        return f"New Signal VIP \n\n " \
                  f"Asset: {instance.symbol}\n" \
                  f"Direction: {instance.side}\n" \
                  f"Entry: {instance.entry_point}\n" \
                  f"Leverage: {instance.leverage}x\n" \
                  f"Volume: {instance.volume}\n\n" \
                  f"TP1: {instance.tp1}\n" \
                  f"TP2: {instance.tp2}\n" \
                  f"TP3: {instance.tp3}\n" \
                  f"TP4: {instance.tp4}\n" \
                  f"TP5: {instance.tp5}\n" \
                  f"🔴STOP LOSS: {instance.stop_loss}"

    @staticmethod
    def get_remove_signal_notif_message(instance: NewSignal) -> str:
        if instance.remove_signal_strategy == NewSignal.CLOSE_1:
            return f"signal by {instance.author_name} on {instance.symbol} have been canceled" \
                   f"\n all position closed all sl and tp on this symbol will cancel soon automatic"
        elif instance.remove_signal_strategy == NewSignal.CLOSE_2:
            return f"signal by {instance.author_name} on {instance.symbol} have been canceled/ removed " \
                   f"\n you can modify it manually ."

    @staticmethod
    def get_modify_signal_message(instance: NewSignal) -> str:
        return f"signal by {instance.author_name} on {instance.symbol} have been modified"

    @staticmethod
    def new_account_message(instance: ExchangeAccounts):
        return f"New Account Added to system " \
               f"\nAccount name :{instance.username}"


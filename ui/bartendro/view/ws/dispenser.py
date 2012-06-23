# -*- coding: utf-8 -*-
from time import sleep
from werkzeug.utils import redirect
from werkzeug.exceptions import BadRequest, ServiceUnavailable
from bartendro.utils import session, local, expose, validate_url, url_for, render_text, log
from bartendro.model.drink import Drink
from bartendro.model.booze import Booze
from bartendro.form.booze import BoozeForm
from bartendro.mixer import CALIBRATION_TICKS

@expose('/ws/dispenser/<int:disp>/on')
def ws_dispenser_on(request, disp):
    driver = local.application.driver
    driver.start(disp - 1)
    return render_text("ok\n")

@expose('/ws/dispenser/<int:disp>/off')
def ws_dispenser_off(request, disp):
    driver = local.application.driver
    driver.stop(disp - 1)
    return render_text("ok\n")

@expose('/ws/dispenser/<int:disp>/test')
def ws_dispenser_test(request, disp):
    driver = local.application.driver
    driver.dispense_ticks(disp - 1, CALIBRATION_TICKS)
    while driver.is_dispensing(disp - 1):
	sleep(.1)
    t, ticks = driver.get_dispense_stats(disp - 1)
    log("Calibration run: %d ms and %d ticks" % (t, ticks))
    return render_text("ok\n")

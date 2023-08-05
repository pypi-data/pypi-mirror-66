# -*- coding: utf-8 -*-
# :Project:   SoL -- Tourney controller
# :Created:   gio 23 ott 2008 11:13:02 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2013, 2014, 2016, 2017, 2018, 2020 Lele Gaifax
#

import logging
import time

from pyramid.httpexceptions import HTTPInternalServerError
from pyramid.view import view_config

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from . import get_request_logger
from ..i18n import country_name, translatable_string as _, ngettext, translator
from ..models import (
    Championship,
    Competitor,
    Match,
    Player,
    Tourney,
    )
from ..models.errors import OperationAborted
from . import expose, unauthorized_for_guest


logger = logging.getLogger(__name__)


@view_config(route_name="tourney_players", renderer="json")
@expose(Player, fields='idplayer,description'.split(','))
def players(request, results):
    return results


@view_config(route_name="competitors", renderer="json")
@expose(
    Competitor,
    fields=('player1FullName,player2FullName,'
            'player3FullName,player4FullName,'
            'player1Nationality,player1Sex,'
            'idcompetitor,retired,idplayer1,'
            'idplayer2,idplayer3,idplayer4,'
            'rate,idtourney,player1LastName,player1FirstName').split(','),
    metadata=dict(
        player1FullName=dict(
            label=_('Player'),
            hint=_('Full name of the player.'),
            lookup=dict(url='/tourney/players?sort_by_lastname=ASC&sort_by_firstname=ASC',
                        idField='idplayer',
                        lookupField='idplayer1',
                        displayField='description',
                        width=200,
                        pageSize=12)),
        player2FullName=dict(
            label=_('2nd player'),
            hint=_('Full name of the second player.'),
            lookup=dict(url='/tourney/players?sort_by_lastname=ASC&sort_by_firstname=ASC',
                        idField='idplayer',
                        lookupField='idplayer2',
                        displayField='description',
                        width=200,
                        pageSize=12)),
        player3FullName=dict(
            label=_('3rd player'),
            hint=_('Full name of the third player.'),
            lookup=dict(url='/tourney/players?sort_by_lastname=ASC&sort_by_firstname=ASC',
                        idField='idplayer',
                        lookupField='idplayer3',
                        displayField='description',
                        width=200,
                        pageSize=12)),
        player4FullName=dict(
            label=_('4th player'),
            hint=_('Full name of the fourth player.'),
            lookup=dict(url='/tourney/players?sort_by_lastname=ASC&sort_by_firstname=ASC',
                        idField='idplayer',
                        lookupField='idplayer4',
                        displayField='description',
                        width=200,
                        pageSize=12)),
        player1Nationality=dict(
            label=_('Nationality'),
            hint=_('First player nationality.'),
            hidden=True,
            readOnly=True),
        player1Sex=dict(
            label=_('Gender'),
            hint=_('Gender of the first player.'),
            hidden=True,
            readOnly=True),
        player1FirstName=dict(
            label=_("First player's name"),
            hint=_("First name of the first player."),
            hidden=True,
            readOnly=True),
        player1LastName=dict(
            label=_("First player's surname"),
            hint=_("Last name of the first player."),
            hidden=True,
            readOnly=True),
        rate=dict(
            label=_('Rate'),
            hint=_('Most recent Glicko rate value of the competitor.'),
            hidden=True,
            readonly=True)
    ))
def competitors(request, results):
    # Add the full name of the first player country, used as an hint
    # on the competitors pane flag icons
    if 'metadata' in results:
        t = translator(request)
        results['metadata']['fields'].append({
            'label': t(_('Country')),
            'hint': t(_('Country name')),
            'name': 'player1Country',
            'hidden': True
        })
    else:
        for r in results['root']:
            code = r['player1Nationality']
            if code:
                r['player1Country'] = country_name(code, request=request)
    return results


_championship_t = Championship.__table__


@view_config(route_name="matches", renderer="json")
@expose(
    Match,
    fields=('board,description,score1,score2'
            ',misses1_1,misses1_2,misses1_3,misses1_4'
            ',misses1_5,misses1_6,misses1_7,misses1_8'
            ',misses2_1,misses2_2,misses2_3,misses2_4'
            ',misses2_5,misses2_6,misses2_7,misses2_8'
            ',turn,final,idmatch,idcompetitor1,idcompetitor2').split(','),
    metadata=dict(
        board=dict(readonly=True, sortable=False, width=70),
        description=dict(label=_('Match'),
                         hint=_('Competitor 1 vs Competitor 2.'),
                         sortable=False,
                         readonly=True,
                         flex=1),
        score1=dict(sortable=False, width=60),
        score2=dict(sortable=False, width=60),
        misses1_1=dict(hidden=True, sortable=False, width=60),
        misses1_2=dict(hidden=True, sortable=False, width=60),
        misses1_3=dict(hidden=True, sortable=False, width=60),
        misses1_4=dict(hidden=True, sortable=False, width=60),
        misses1_5=dict(hidden=True, sortable=False, width=60),
        misses1_6=dict(hidden=True, sortable=False, width=60),
        misses1_7=dict(hidden=True, sortable=False, width=60),
        misses1_8=dict(hidden=True, sortable=False, width=60),
        misses2_1=dict(hidden=True, sortable=False, width=60),
        misses2_2=dict(hidden=True, sortable=False, width=60),
        misses2_3=dict(hidden=True, sortable=False, width=60),
        misses2_4=dict(hidden=True, sortable=False, width=60),
        misses2_5=dict(hidden=True, sortable=False, width=60),
        misses2_6=dict(hidden=True, sortable=False, width=60),
        misses2_7=dict(hidden=True, sortable=False, width=60),
        misses2_8=dict(hidden=True, sortable=False, width=60),
        turn=dict(hidden=True, readonly=True, sortable=False, width=70),
        final=dict(hidden=True, readonly=True, sortable=False),
        idmatch=dict(sortable=False),
        idcompetitor1=dict(sortable=False),
        idcompetitor2=dict(sortable=False),
    ))
def matches():
    request, args = (yield)
    results = yield args

    q = (select([_championship_t.c.trainingboards],
                from_obj=_championship_t.join(_tourneys_t))
         .where(_tourneys_t.c.idtourney == int(request.params['filter_by_idtourney'])))
    tboards = request.dbsession.scalar(q) or 0

    root = results.get('root')
    if root:
        # This is a mere optimization, removing pointless NULL values
        for match in root:
            for i in range(tboards+1, 9):
                del match[f'misses1_{i}']
                del match[f'misses2_{i}']

    md = results.get('metadata')
    if md:
        if tboards:
            # We MUST do this, due to ExtJS4 editable grid glitches
            fields = md['fields']
            remove_fields = set()
            for i in range(tboards+1, 9):
                remove_fields.add(f'misses1_{i}')
                remove_fields.add(f'misses2_{i}')
            for i in range(len(fields)-1, -1, -1):
                if fields[i]['name'] in remove_fields:
                    del fields[i]

    yield results


@view_config(route_name="ranking", renderer="json", request_param="turn")
def rankingForTurn(request):
    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['filter_by_idtourney'])
        turn = int(params['turn'])

        tourney = sess.query(Tourney).get(idtourney)

        ranking = [dict(rank=i, idcompetitor=c.idcompetitor, description=c.description,
                        points=r.points, netscore=r.netscore, totscore=r.totscore,
                        bucholz=r.bucholz, rate=r.rate, prize=0,
                        player1Nationality=c.player1Nationality)
                   for i, (c, r) in enumerate(tourney.computeRanking(turn), 1)]

        return dict(success=True, message='Ok', count=len(ranking), root=ranking)
    except Exception as e:  # pragma: no cover
        message = str(e)
        get_request_logger(request, logger).critical("Couldn't compute ranking: %s", message,
                                                     exc_info=True)
        return dict(success=False, message=message)


@view_config(route_name="ranking", renderer="json")
@expose(Query([Competitor]),
        fields=('description,points,bucholz,netscore,prize,totscore,'
                'rate,player1Nationality,idcompetitor').split(','),
        metadata=dict(
    description=dict(label=_('Competitor'),
                     hint=_('Full name of the players.'),
                     sortable=False,
                     readonly=True,
                     flex=1),
    points=dict(readonly=True, width=40, sortable=False),
    bucholz=dict(readonly=True, width=40, sortable=False),
    netscore=dict(readonly=True, width=40, sortable=False),
    totscore=dict(hidden=True, readonly=True, width=40, sortable=False),
    prize=dict(hidden=True, width=55, sortable=False, decimals=2, type='numeric'),
    rate=dict(label=_('Rate'),
              hint=_('Most recent Glicko rate of the competitor (if'
                     ' tourney is associated with a rating).'),
              hidden=True,
              align='right',
              type='integer',
              readonly=True,
              width=50),
    player1Nationality=dict(label=_('Nationality'),
                            hint=_('Nationality of the competitor.'),
                            hidden=True,
                            readonly=True,
                            width=40)
    ))
def ranking(request, results):
    from operator import itemgetter

    t = translator(request)
    if 'metadata' in results:
        results['metadata']['fields'].insert(0, {
            'label': t(_('Rank')),
            'hint': t(_('Position in the ranking.')),
            'width': 30,
            'readonly': True,
            'name': 'rank',
            'align': 'right',
            'type': 'integer'})
    else:
        ranking = results['root']
        # Match the local ordering applied by the Ranking panel, so the "rank" field is
        # reasonable: by ascending player's name, then by descending ranking position.
        ranking.sort(key=itemgetter('description'))
        ranking.sort(key=itemgetter('prize', 'points', 'bucholz',
                                    'netscore', 'totscore', 'rate'),
                     reverse=True)
        for i, r in enumerate(ranking, 1):
            r['rank'] = i
    return results


_matches_t = Match.__table__
_tourneys_t = Tourney.__table__


@view_config(route_name="boards", renderer="json")
@expose(Query([Match])
        .filter(_matches_t.c.turn == _tourneys_t.c.currentturn)
        .filter(_matches_t.c.idtourney == _tourneys_t.c.idtourney)
        .order_by(_matches_t.c.board),
        fields=('board,idcompetitor1,competitor1FullName,'
                'idcompetitor2,competitor2FullName,idmatch,'
                'idtourney,score1,score2,competitor1Opponents,'
                'competitor2Opponents').split(','))
def boards(request, results):
    return results


@view_config(route_name="delete_from_turn", renderer="json")
@unauthorized_for_guest
def deleteFromTurn(request):
    "Delete already played turns, recomputing the ranking."

    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])
        fromturn = int(params['fromturn'])

        tourney = sess.query(Tourney).get(idtourney)

        if tourney.prized:
            tourney.resetPrizes()

        delmatches = [m for m in tourney.matches if m.turn >= fromturn]
        for match in delmatches:
            sess.delete(match)

        tourney.currentturn = fromturn-1
        if tourney.finalturns:
            tourney.finalturns = any(m for m in tourney.matches
                                     if m.turn < fromturn and m.final)
        tourney.countdownstarted = None
        sess.flush()

        # recompute the ranking
        sess.expunge(tourney)
        tourney = sess.query(Tourney).get(idtourney)
        tourney.updateRanking()
        sess.flush()

        success = True
        message = 'Ok'
    except Exception as e:  # pragma: no cover
        message = str(e)
        get_request_logger(request, logger).critical("Couldn't delete turns: %s", message,
                                                     exc_info=True)
        success = False

    return dict(success=success, message=message,
                currentturn=tourney.currentturn,
                rankedturn=tourney.rankedturn,
                finalturns=tourney.finalturns,
                prized=tourney.prized)


@view_config(route_name="new_turn", renderer="json")
@unauthorized_for_guest
def newTurn(request):
    "Create next turn, if possible."

    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])

        tourney = sess.query(Tourney).get(idtourney)
        tourney.makeNextTurn()

        sess.flush()

        success = True
        message = 'Ok'
    except OperationAborted as e:  # pragma: no cover
        errormsg = e.args[0]
        get_request_logger(request, logger).error("Couldn't create next turn: %s", errormsg)
        message = request.localizer.translate(errormsg)
        success = False
    except Exception as e:  # pragma: no cover
        message = str(e)
        get_request_logger(request, logger).critical("Couldn't create next turn: %s",
                                                     message, exc_info=True)
        success = False

    return dict(success=success, message=message,
                currentturn=tourney.currentturn,
                rankedturn=tourney.rankedturn,
                finalturns=tourney.finalturns,
                prized=tourney.prized)


@view_config(route_name="send_training_urls", renderer="json")
@unauthorized_for_guest
def sendTrainingURLs(request):
    sess = request.dbsession
    params = request.params
    idtourney = int(params['idtourney'])

    tourney = sess.query(Tourney).get(idtourney)
    if tourney is not None and tourney.championship.trainingboards:
        tourney.sendTrainingURLs(request)
        return dict(success=True, message="Ok")
    else:
        return dict(success=False,
                    message=request.localizer.translate(_("Bad request!")))


@view_config(route_name="final_turn", renderer="json")
@unauthorized_for_guest
def finalTurn(request):
    "Create final turn."

    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])

        tourney = sess.query(Tourney).get(idtourney)
        tourney.makeFinalTurn()

        sess.flush()

        success = True
        message = 'Ok'
    except OperationAborted as e:  # pragma: no cover
        errormsg = e.args[0]
        get_request_logger(request, logger).error("Couldn't create final turn: %s", errormsg)
        message = request.localizer.translate(errormsg)
        success = False
    except Exception as e:  # pragma: no cover
        message = str(e)
        get_request_logger(request, logger).critical("Couldn't create final turn: %s",
                                                     message, exc_info=True)
        success = False

    return dict(success=success, message=message,
                currentturn=tourney.currentturn,
                rankedturn=tourney.rankedturn,
                finalturns=tourney.finalturns,
                prized=tourney.prized)


@view_config(route_name="update_ranking", renderer="json")
@unauthorized_for_guest
def updateRanking(request):
    "Recompute current ranking."

    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])

        tourney = sess.query(Tourney).get(idtourney)
        tourney.updateRanking()

        sess.flush()

        success = True
        message = 'Ok'
    except OperationAborted as e:  # pragma: no cover
        errormsg = e.args[0]
        get_request_logger(request, logger).error("Couldn't update the ranking: %s", errormsg)
        message = request.localizer.translate(errormsg)
        success = False
    except Exception as e:  # pragma: no cover
        message = str(e)
        get_request_logger(request, logger).critical("Couldn't update the ranking: %s",
                                                     message, exc_info=True)
        success = False
    return dict(success=success, message=message,
                currentturn=tourney.currentturn,
                rankedturn=tourney.rankedturn,
                finalturns=tourney.finalturns,
                prized=tourney.prized)


@view_config(route_name="assign_prizes", renderer="json")
@unauthorized_for_guest
def assignPrizes(request):
    "Assign final prizes."

    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])

        tourney = sess.query(Tourney).get(idtourney)
        tourney.assignPrizes()

        if tourney.rating is not None:
            tourney.rating.recompute(tourney.date)

        sess.flush()

        success = True
        message = 'Ok'
    except Exception as e:  # pragma: no cover
        message = str(e)
        get_request_logger(request, logger).critical("Couldn't assign prizes: %s", message,
                                                     exc_info=True)
        success = False
    return dict(success=success, message=message,
                currentturn=tourney.currentturn,
                rankedturn=tourney.rankedturn,
                finalturns=tourney.finalturns,
                prized=tourney.prized)


@view_config(route_name="reset_prizes", renderer="json")
@unauthorized_for_guest
def resetPrizes(request):
    "Reset assigned final prizes."

    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])

        tourney = sess.query(Tourney).get(idtourney)
        tourney.resetPrizes()

        sess.flush()

        success = True
        message = 'Ok'
    except Exception as e:  # pragma: no cover
        message = str(e)
        get_request_logger(request, logger).critical("Couldn't reset prizes: %s", message,
                                                     exc_info=True)
        success = False
    return dict(success=success, message=message,
                currentturn=tourney.currentturn,
                rankedturn=tourney.rankedturn,
                finalturns=tourney.finalturns,
                prized=tourney.prized)


@view_config(route_name="replay_today", renderer="json")
@unauthorized_for_guest
def replayToday(request):
    "Replicate the given tourney today."

    from datetime import date

    t = translator(request)

    new_idtourney = None
    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])

        tourney = sess.query(Tourney).get(idtourney)
        new = tourney.replay(date.today(), request.session['user_id'])

        sess.flush()

        new_idtourney = new.idtourney
        success = True
        message = t(_('Created "$tourney" in championship "$championship"',
                      mapping=dict(tourney=new.description,
                                   championship=new.championship.description)))
    except IntegrityError:  # pragma: no cover
        message = t(_('Could not duplicate the tourney because there is'
                      ' already an event today, sorry!'))
        get_request_logger(request, logger).error("Couldn't duplicate tourney:"
                                                  " there is already an event today, sorry!")
        success = False
    except Exception as e:  # pragma: no cover
        message = str(e)
        get_request_logger(request, logger).critical("Couldn't duplicate tourney: %s",
                                                     message, exc_info=True)
        success = False
    return dict(success=success, message=message, new_idtourney=new_idtourney)


@view_config(route_name="countdown", request_method="POST", renderer="json")
def countdownStarted(request):
    "Register the countdown start timestamp."

    curruser = request.session.get('user_id', '*nouser*')

    sess = request.dbsession
    params = request.params
    idtourney = int(params['idtourney'])
    if 'start' in params:
        start = int(params['start'])
    else:
        start = None
    tourney = sess.query(Tourney).get(idtourney)
    if not tourney.prized and curruser == tourney.idowner:
        tourney.countdownstarted = start
        logger.debug("Countdown for %s %s",
                     repr(tourney),
                     'terminated' if start is None else 'started')
        return dict(success=True,
                    message="Ok, countdown %s" % ('terminated' if start is None
                                                  else 'started'))
    else:
        get_request_logger(request, logger).warning(
            "Attempt to start/stop countdown for %s ignored", repr(tourney))
        return dict(success=False, message="Tourney is prized, or not owned by you")


@view_config(route_name="countdown", renderer="countdown.mako")
def countdown(request):
    "Show the game countdown."

    from ..printouts.utils import ordinal

    t = translator(request)

    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])

        tourney = sess.query(Tourney).get(idtourney)
        curruser = request.session.get('user_id', '*nouser*')
        now = int(time.time() * 1000)
        starttime = tourney.countdownstarted
        if starttime and (starttime + tourney.duration * 60 * 1000) < now:
            starttime = None
        return dict(
            _=t,
            ngettext=ngettext,
            duration=tourney.duration,
            prealarm=tourney.prealarm,
            currentturn=ordinal(tourney.currentturn),
            starttime=starttime,
            notifystart=request.path_qs,
            isowner=curruser == tourney.idowner)
    except Exception as e:  # pragma: no cover
        get_request_logger(request, logger).critical("Couldn't show the countdown: %s", e,
                                                     exc_info=True)
        raise HTTPInternalServerError(str(e))


@view_config(route_name="pre_countdown", renderer="pre_countdown.mako")
def pre_countdown(request):
    "Show a countdown while preparing the next round."

    from ..printouts.utils import ordinal

    t = translator(request)

    try:
        sess = request.dbsession
        params = request.params
        idtourney = int(params['idtourney'])
        duration = int(params['duration'])
        prealarm = int(params['prealarm'])

        tourney = sess.query(Tourney).get(idtourney)
        return dict(
            _=t,
            ngettext=ngettext,
            duration=duration,
            prealarm=prealarm,
            nextturn=ordinal(tourney.currentturn+1))
    except Exception as e:  # pragma: no cover
        get_request_logger(request, logger).critical("Couldn't show the countdown: %s", e,
                                                     exc_info=True)
        raise HTTPInternalServerError(str(e))

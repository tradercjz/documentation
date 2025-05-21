#!/usr/bin/env python
# coding: utf-8

def query(session, startDate, endDate, cols='"*"', security='NULL'):
    script = 'query({}, {}, {}, {})'.format(startDate, endDate, cols, security)
    return session.run(script)

def queryRecentYear(session, startDate='NULL', endDate='NULL', cols='"*"', security='NULL'):
    script = 'queryRecentYear({}, {}, {}, {})'.format(startDate, endDate, cols, security)
    return session.run(script)

def queryFirst10Col(session, startDate, endDate, cols='NULL', security='NULL'):
    script = 'queryFirst10Col({}, {}, {}, {})'.format(startDate, endDate, cols, security)
    return session.run(script)

def queryCond(session, startDate, endDate, cols='NULL', security='NULL'):
    script = 'queryCond({}, {}, {}, {})'.format(startDate, endDate, cols, security)
    return session.run(script)
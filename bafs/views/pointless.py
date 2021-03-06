from bafs import app, db, data
from flask import render_template
from sqlalchemy import text

def averagespeed():
	q = text("""
		select a.id, a.display_name, avg(b.average_speed) as speed from athletes a, rides b where a.id = b.athlete_id group by a.id order by speed;
		""")
	avgspeed = [(x['id'], x['display_name'], x['speed']) for x in db.session.execute(q).fetchall()]	
	return render_template('people/averagespeed.html', avg = avgspeed)

def shortride():
	q = text("""
		select a.id, a.display_name, avg(b.distance) as dist, count(distinct(date(b.start_date))) as distrides from athletes a, 
		rides b where a.id = b.athlete_id group by a.id order by dist;
		""")
	avgdist = [(x['id'], x['display_name'], x['dist']) for x in db.session.execute(q).fetchall() if x['distrides']>=10]	
	return render_template('people/distance.html', avg = avgdist) 

def billygoat():
	q = text("""
	select sum(a.elevation_gain) as elev,sum(a.distance) as dist, (sum(a.elevation_gain)/sum(a.distance)) as gainpermile, 
	c.name from rides a, athletes b, teams c where a.athlete_id=b.id and b.team_id=c.id group by c.name order by gainpermile desc;
	""")
	goat = [(x['name'], x['gainpermile'],x['dist'],x['elev']) for x in db.session.execute(q).fetchall()]
	return render_template('people/billygoat.html', data = goat)

def tortoiseteam():
	q = text("""
	select avg(a.average_speed) as spd,	c.name from rides a, athletes b, teams c where a.athlete_id=b.id and b.team_id=c.id group by c.name order by spd asc;
	""")
	goat = [(x['name'], x['spd']) for x in db.session.execute(q).fetchall()]
	return render_template('people/tortoiseteam.html', data = goat)
	
def weekendwarrior():
	q = text("""
		select A.id as athlete_id, A.display_name as athlete_name, sum(DS.points) as total_score, 
		sum(if((dayofweek(DS.ride_date)=7 or (dayofweek(DS.ride_date)=1)) , DS.points, 0)) as 'weekend',
		sum(if((dayofweek(DS.ride_date)<7 and (dayofweek(DS.ride_date)>1)) , DS.points, 0)) as 'weekday' 
		from daily_scores DS join athletes A on A.id = DS.athlete_id group by A.id
		order by weekend desc;
		""")
	weekend = [(x['athlete_id'], x['athlete_name'], x['total_score'], x['weekend'], x['weekday']) for x in db.session.execute(q).fetchall()]
	return render_template('people/weekend.html', data = weekend)

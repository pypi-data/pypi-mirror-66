query = '''
with x as (select
  PERCENTILE_DISC(offer.preisProQm, 0.5) OVER(PARTITION BY geo.koordinaten) as med_price,
  count(offer.preisproqm) over(partition by geo.koordinaten) as counts,
  STDDEV_POP(offer.preisProQm) OVER(PARTITION BY geo.koordinaten) as stdprice,
  avg(offer.preisproqm) - (VAR_POP(offer.preisproqm + 1) / 2) as drift,
  geo.koordinaten as coords,
  geo.wohnquartierskennziffer as kz,
  ROW_NUMBER() OVER(PARTITION BY geo.wohnquartierskennziffer ORDER BY geo.wohnquartierskennziffer) as name
  from offerData.offerData as offer
  join geoData.nexigaWohnquartiereGeoData as geo
  on ST_CONTAINS(ST_GEOGFROMTEXT(geo.koordinaten),ST_GEOGPOINT(CAST(offer.latitude AS FLOAT64),CAST(offer.longitude AS FLOAT64)))
  where offer.ort = '{}'
  group by geo.koordinaten, geo.wohnquartiersKennziffer, offer.preisProQm
  )
  select
  x.kz,
  med_price,
  stdprice,
  coords,
  x.counts,
  avg(s22.kaufkraftIndexBrd100) as kaufkraft,
  1 - COALESCE((avg(s22.arbeitsloseInsgesamt) - min(s22.arbeitsloseInsgesamt))  / NULLIF((max(s22.arbeitsloseInsgesamt) - min(s22.arbeitsloseInsgesamt)),0), 0) as employed,
  (avg(s22.zuzuegeInsgesamtEinwohner + 0.001) / avg(s22.einwohnerinsgesamt + 0.001)) - (avg(s22.fortzuegeIngesamtEinwohner + 0.001) / avg(s22.einwohnerinsgesamt + 0.001)) as moveinout,
  avg(s22.income_9)as income_9,
  avg(s22.income_9_15) as income_9_15,
  avg(s22.income_15_26) as income_15_26,
  avg(s22.income_26_36) as income_26_36,
  avg(s22.income_36_50) as income_36_50,
  avg(s22.income_50) as income_50,
  avg(s36.passantenFrequenzScore) as movement,
  sum(IF(s44.baujahresklasseEinesHauses = 'vor1900',1,0)) as rank0,
  sum(IF(s44.baujahresklasseEinesHauses = '1900Bis1945',1,0)) as rank1,
  sum(IF(s44.baujahresklasseEinesHauses = '1946Bis1960',1,0)) as rank2,
  sum(IF(s44.baujahresklasseEinesHauses = '1961Bis1970',1,0)) as rank3,
  sum(IF(s44.baujahresklasseEinesHauses = '1971Bis1980',1,0)) as rank4,
  sum(IF(s44.baujahresklasseEinesHauses = '1981Bis1985',1,0)) as rank5,
  sum(IF(s44.baujahresklasseEinesHauses = '1986Bis1995',1,0)) as rank6,
  sum(IF(s44.baujahresklasseEinesHauses = '1996Bis2000',1,0)) as rank7,
  sum(IF(s44.baujahresklasseEinesHauses = '2001Bis2005',1,0)) as rank8,
  sum(IF(s44.baujahresklasseEinesHauses = '2006Bis2010',1,0)) as rank9,
  sum(IF(s44.baujahresklasseEinesHauses = 'ab2016',1,0)) as rank10,

  sum(IF(s44.gebaeudecharakteristik = 'Wohnblock',1,0)) as living1,
  sum(IF(s44.gebaeudecharakteristik = 'Mehrfamilienhaus',1,0)) as living2,
  sum(IF(s44.gebaeudecharakteristik = 'Terrassenhaus',1,0)) as living3,

  sum(IF(s44.gebaeudecharakteristik = 'reihenOderDoppelhaus',1,0)) as living_1_1,
  sum(IF(s44.gebaeudecharakteristik = 'einOderZweifamilienhaus',1,0)) as living_1_2,

  sum(IF(s44.gebaeudecharakteristik = 'fabrikLagergebaeude',1,0)) as living_2_1,
  sum(IF(s44.gebaeudecharakteristik = 'Büro',1,0)) as living_2_2


  from x
  join
  (select haushalteMitMonatlichemNettoeinkommen0Bis900Euro as income_9,
  haushalteMitMonatlichemNettoeinkommen900Bis1500Euro as income_9_15,
  haushalteMitMonatlichemNettoeinkommen1500Bis2600Euro as income_15_26,
  haushalteMitMonatlichemNettoeinkommen2600Bis3600Euro as income_26_36,
  haushalteMitMonatlichemNettoeinkommen3600Bis5000Euro as income_36_50,
  haushalteMitMonatlichemNettoeinkommenAb5000Euro as income_50,
  wohnquartierskennziffer,kaufkraftIndexBrd100,  einpendler, auspendler, arbeitsloseInsgesamt, fortzuegeIngesamtEinwohner, zuzuegeInsgesamtEinwohner, einwohnerinsgesamt
  from socialdemographicData.nexigaKgs22Data2019
  union all
  select haushalteMitMonatlichemNettoeinkommen0Bis900Euro as income_9,
  haushalteMitMonatlichemNettoeinkommen900Bis1500Euro as income_9_15,
  haushalteMitMonatlichemNettoeinkommen1500Bis2600Euro as income_15_26,
  haushalteMitMonatlichemNettoeinkommen2600Bis3600Euro as income_26_36,
  haushalteMitMonatlichemNettoeinkommen3600Bis5000Euro as income_36_50,
  haushalteMitMonatlichemNettoeinkommenAb5000Euro as income_50, wohnquartierskennziffer,kaufkraftIndexBrd100, einpendler, auspendler, arbeitsloseInsgesamt, fortzuegeIngesamtEinwohner, zuzuegeInsgesamtEinwohner, einwohnerinsgesamt
  from socialdemographicData.nexigaKgs22Data2015
  union all
  select haushalteMitMonatlichemNettoeinkommen0Bis900Euro as income_9,
  haushalteMitMonatlichemNettoeinkommen900Bis1500Euro as income_9_15,
  haushalteMitMonatlichemNettoeinkommen1500Bis2600Euro as income_15_26,
  haushalteMitMonatlichemNettoeinkommen2600Bis3600Euro as income_26_36,
  haushalteMitMonatlichemNettoeinkommen3600Bis5000Euro as income_36_50,
  haushalteMitMonatlichemNettoeinkommenAb5000Euro as income_50, wohnquartierskennziffer, kaufkraftIndexBrd100, einpendler, auspendler, arbeitsloseInsgesamt, fortzuegeIngesamtEinwohner, einwohnerinsgesamt, zuzuegeInsgesamtEinwohner
  from socialdemographicData.nexigaKgs22Data2016
  union all
  select haushalteMitMonatlichemNettoeinkommen0Bis900Euro as income_9,
  haushalteMitMonatlichemNettoeinkommen900Bis1500Euro as income_9_15,
  haushalteMitMonatlichemNettoeinkommen1500Bis2600Euro as income_15_26,
  haushalteMitMonatlichemNettoeinkommen2600Bis3600Euro as income_26_36,
  haushalteMitMonatlichemNettoeinkommen3600Bis5000Euro as income_36_50,
  haushalteMitMonatlichemNettoeinkommenAb5000Euro as income_50, wohnquartierskennziffer, kaufkraftIndexBrd100,einpendler, auspendler, arbeitsloseInsgesamt, fortzuegeIngesamtEinwohner, zuzuegeInsgesamtEinwohner, einwohnerinsgesamt
  from socialdemographicData.nexigaKgs22Data2017
  union all
  select haushalteMitMonatlichemNettoeinkommen0Bis900Euro as income_9,
  haushalteMitMonatlichemNettoeinkommen900Bis1500Euro as income_9_15,
  haushalteMitMonatlichemNettoeinkommen1500Bis2600Euro as income_15_26,
  haushalteMitMonatlichemNettoeinkommen2600Bis3600Euro as income_26_36,
  haushalteMitMonatlichemNettoeinkommen3600Bis5000Euro as income_36_50,
  haushalteMitMonatlichemNettoeinkommenAb5000Euro as income_50, wohnquartierskennziffer, kaufkraftIndexBrd100, einpendler, auspendler, arbeitsloseInsgesamt, fortzuegeIngesamtEinwohner, zuzuegeInsgesamtEinwohner, einwohnerinsgesamt
  from socialdemographicData.nexigaKgs22Data2018
  ) s22 on s22.wohnquartierskennziffer = x.kz
  join
  (select wohnquartierskennziffer, passantenfrequenzscore
  from socialdemographicData.nexigaKgs36Data2019
  union all
  select wohnquartierskennziffer, passantenfrequenzscore
  from socialdemographicData.nexigaKgs36Data2015
  union all
  select wohnquartierskennziffer, passantenfrequenzscore
  from socialdemographicData.nexigaKgs36Data2016
  union all
  select wohnquartierskennziffer, passantenfrequenzscore
  from socialdemographicData.nexigaKgs36Data2017
  union all
  select wohnquartierskennziffer, passantenfrequenzscore
  from socialdemographicData.nexigaKgs36Data2018
  ) s36 on s36.wohnquartierskennziffer = x.kz
  join
  socialdemographicData.nexigaKgs44Data2019 as s44
  on s44.wohnquartierskennziffer = x.kz
  where name = 1
  group by
  x.kz,
  med_price,
  coords,
  x.counts,
  drift,
  stdprice
'''

# Garden vs 3502 — Actual Source Comparison

- Garden actual source entries after Garden filters: **410**
- 3502 actual source: **https://iptv-org.github.io/iptv/index.m3u**
- Matching rule: **exact stream URL**
- Different/Not Found rule: channel name is used only after exact URL is absent.

- Same: **410**
- Different URL: **0**
- Not Found: **0**

## Business

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | CNBC Awaaz | https://n18syndication.akamaized.net/bpk-tv/CNBC_Awaaz_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/CNBC_Awaaz_NW18_MOB/output01/master.m3u8 |
| Working | Same | Zee Business | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zee_business/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/af1b3fa3-f56d-4741-9c63-78409a798988/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zee_business/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/af1b3fa3-f56d-4741-9c63-78409a798988/main.m3u8 |
| Working | Same | CNBC Bajar | https://n18syndication.akamaized.net/bpk-tv/CNBC_Bazaar_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/CNBC_Bazaar_NW18_MOB/output01/master.m3u8 |
| Working | Same | CNBC TV18 | https://n18syndication.akamaized.net/bpk-tv/CNBC_TV18_NW18_MOB/output01/index.m3u8 | https://n18syndication.akamaized.net/bpk-tv/CNBC_TV18_NW18_MOB/output01/index.m3u8 |
| Working | Same | CNBC TV18 Prime HD | https://n18syndication.akamaized.net/bpk-tv/CNBC_Tv18_Prime_HD_NW18_MOB/output01/index.m3u8 | https://n18syndication.akamaized.net/bpk-tv/CNBC_Tv18_Prime_HD_NW18_MOB/output01/index.m3u8 |
| Non-working | Same | ET Now (720p) | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/etnow/etnow_master.m3u8 | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/etnow/etnow_master.m3u8 |
| Non-working | Same | ET Now Swadesh (1080p) | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/etswadesh/etswadesh_master.m3u8 | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/etswadesh/etswadesh_master.m3u8 |

## Cartoon

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Non-working | Same | Cartoon Network HD+ | http://103.135.253.32:8080/CN-NETWORK/index.m3u8 | http://103.135.253.32:8080/CN-NETWORK/index.m3u8 |
| Non-working | Same | Doraemon | https://live20.bozztv.com/giatvplayout7/giatv-209902/tracks-v1a1/mono.ts.m3u8 | https://live20.bozztv.com/giatvplayout7/giatv-209902/tracks-v1a1/mono.ts.m3u8 |
| Working | Same | Epic Kids Digital | https://cc-t8lqe1o99pszu.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-t8lqe1o99pszu/playlist.m3u8 | https://cc-t8lqe1o99pszu.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-t8lqe1o99pszu/playlist.m3u8 |
| Working | Same | Green Gold TV | https://cc-szrmqvu8zkg16.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-szrmqvu8zkg16/greengold/stream/grngld/playlist.m3u8 | https://cc-szrmqvu8zkg16.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-szrmqvu8zkg16/greengold/stream/grngld/playlist.m3u8 |
| Non-working | Same | Nick Jr. (India) | http://103.185.24.134:3001/NICK-JR/index.m3u8 | http://103.185.24.134:3001/NICK-JR/index.m3u8 |
| Non-working | Same | Nickelodeon (India) | http://103.185.24.134:3001/NICK/index.m3u8 | http://103.185.24.134:3001/NICK/index.m3u8 |
| Non-working | Same | Pogo | http://103.135.253.32:8080/POGO/index.m3u8 | http://103.135.253.32:8080/POGO/index.m3u8 |
| Non-working | Same | Shin-chan | https://live20.bozztv.com/giatvplayout7/giatv-210780/index.m3u8 | https://live20.bozztv.com/giatvplayout7/giatv-210780/index.m3u8 |
| Non-working | Same | Sonic | http://103.185.24.134:3001/SONIC/index.m3u8 | http://103.185.24.134:3001/SONIC/index.m3u8 |
| Non-working | Same | Sony Yay! | https://livetv.shamon-cable.net:8443/sony_yay/index.m3u8 | https://livetv.shamon-cable.net:8443/sony_yay/index.m3u8 |
| Working | Same | The Jungle Book | https://cc-4bhi5osabejc9.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-4bhi5osabejc9/junglebook.m3u8 | https://cc-4bhi5osabejc9.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-4bhi5osabejc9/junglebook.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment;Kids",Unique TV | https://fta.ektv.in/live/688/master.m3u8 | https://fta.ektv.in/live/688/master.m3u8 |
| Working | Same | WOW Kidz | https://yuppparoriglin.akamaized.net/181224/smil:wowkidzhindi.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yuppparoriglin.akamaized.net/181224/smil:wowkidzhindi.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | ZB Cartoon | https://server.zillarbarta.com/zbcatun/video.m3u8 | https://server.zillarbarta.com/zbcatun/video.m3u8 |

## Devotional

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | Aadinath TV | https://cdn.pishow.tv/ott/live/252/master.m3u8 | https://cdn.pishow.tv/ott/live/252/master.m3u8 |
| Working | Same | Aastha | https://cdn.pishow.tv/ott/live/1454/master.m3u8 | https://cdn.pishow.tv/ott/live/1454/master.m3u8 |
| Working | Same | Aastha HD | https://aasthaott.akamaized.net/110923/smil:aasthatv.smil/index.m3u8 | https://aasthaott.akamaized.net/110923/smil:aasthatv.smil/index.m3u8 |
| Non-working | Same | Aastha UK | https://aasthaott.akamaized.net/110923/smil:aasthauk.smil/playlist.m3u8 | https://aasthaott.akamaized.net/110923/smil:aasthauk.smil/playlist.m3u8 |
| Working | Same | Aastha Bhajan | https://d2lk5u59tns74c.cloudfront.net/out/v1/218f9e64bdce42369500e93cff50572f/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/218f9e64bdce42369500e93cff50572f/index.m3u8 |
| Working | Same | Aastha International | https://aasthaott.akamaized.net/110923/smil:aasthausa.smil/playlist.m3u8 | https://aasthaott.akamaized.net/110923/smil:aasthausa.smil/playlist.m3u8 |
| Non-working | Same | Aastha Prime 1 | https://aasthaott.akamaized.net/110923/smil:aasthaprime1.smil/master.m3u8 | https://aasthaott.akamaized.net/110923/smil:aasthaprime1.smil/master.m3u8 |
| Working | Same | ABN TV India | https://mediaserver.abnvideos.com/streams/abntvindia.m3u8 | https://mediaserver.abnvideos.com/streams/abntvindia.m3u8 |
| Working | Same | Adhyatm TV | https://mumbai-edge.smartplaytv.in/AdhyatmTV/index.m3u8 | https://mumbai-edge.smartplaytv.in/AdhyatmTV/index.m3u8 |
| Working | Same | Anand TV (India) | https://live.legitpro.co.in/anandtv/index.m3u8 | https://live.legitpro.co.in/anandtv/index.m3u8 |
| Non-working | Same | Anand Wari TV | https://mumt03.tangotv.in/Dsly5z3HANANDWARITV/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HANANDWARITV/index.m3u8 |
| Non-working | Same | Aradana TV | https://mumbai-edge.smartplaytv.in/AradanaTV/index.m3u8 | https://mumbai-edge.smartplaytv.in/AradanaTV/index.m3u8 |
| Working | Same | Awakening TV | https://d2gvyg6lvauoko.cloudfront.net/230226/awakeningtv/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://d2gvyg6lvauoko.cloudfront.net/230226/awakeningtv/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | Bhakti Dhara | https://newsliveindia.com:4433/bhaktidhara/index.m3u8 | https://newsliveindia.com:4433/bhaktidhara/index.m3u8 |
| Working | Same | Bhakti Sagar | https://mumt05.tangotv.in/87NeALx2BHAKTISAGAR/index.m3u8 | https://mumt05.tangotv.in/87NeALx2BHAKTISAGAR/index.m3u8 |
| Working | Same | Channel Divya | https://vg-pitaaratvlive.akamaized.net/v1/vglive-sk-906482/playlist.m3u8 | https://vg-pitaaratvlive.akamaized.net/v1/vglive-sk-906482/playlist.m3u8 |
| Working | Same | Darshan 24 | https://mumt05.tangotv.in/87NeALx2DARSHAN24/index.m3u8 | https://mumt05.tangotv.in/87NeALx2DARSHAN24/index.m3u8 |
| Working | Same | Dharm Sandesh | https://d2lk5u59tns74c.cloudfront.net/out/v1/aed713462c734923aac946a547265288/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/aed713462c734923aac946a547265288/index.m3u8 |
| Working | Same | Dheeran TV | https://live.we2live.in/dheerantv/dheerantv/playlist.m3u8 | https://live.we2live.in/dheerantv/dheerantv/playlist.m3u8 |
| Working | Same | Fateh TV | https://stream.ottlive.co.in/fatehtv/index.m3u8 | https://stream.ottlive.co.in/fatehtv/index.m3u8 |
| Working | Same | FGN Channel | https://samitaorigin.tangotv.in/FGNCHANNEL/SAMITAORIGIN/index.m3u8 | https://samitaorigin.tangotv.in/FGNCHANNEL/SAMITAORIGIN/index.m3u8 |
| Working | Same | God Stands TV Hindi | https://online.godstands.tv:5443/WebRTCApp/streams/HindiStreaming.m3u8 | https://online.godstands.tv:5443/WebRTCApp/streams/HindiStreaming.m3u8 |
| Working | Same | GurSikh Sabha TV (720p) | http://cdn12.henico.net:8080/live/gsctv/index.m3u8 | http://cdn12.henico.net:8080/live/gsctv/index.m3u8 |
| Working | Same | Hare Krsna TV | https://hktv.harekrsnatv.com/HKTV/HKWebApp/manifest.mpd | https://hktv.harekrsnatv.com/HKTV/HKWebApp/manifest.mpd |
| Non-working | Same | Hosanna TV Hindi | https://mumbai-edge.smartplaytv.in/HosannaTV/index.m3u8 | https://mumbai-edge.smartplaytv.in/HosannaTV/index.m3u8 |
| Working | Same | Ishwar Bhakti TV | https://6n3yow8pl9ok-hls-live.5centscdn.com/ishwartvlive/tv.stream/playlist.m3u8 | https://6n3yow8pl9ok-hls-live.5centscdn.com/ishwartvlive/tv.stream/playlist.m3u8 |
| Working | Same | Jinvani Channel | https://cdn.pishow.tv/ott/live/989/master.m3u8 | https://cdn.pishow.tv/ott/live/989/master.m3u8 |
| Working | Same | Kanshi TV (720p) | https://live.kanshitv.co.uk/mobile/kanshitvkey.m3u8 | https://live.kanshitv.co.uk/mobile/kanshitvkey.m3u8 |
| Working | Same | LLBN TV South Asia | https://brightstar-southasia-pull-secure.akamaized.net/brightstarsouthasia/stream.m3u8 | https://brightstar-southasia-pull-secure.akamaized.net/brightstarsouthasia/stream.m3u8 |
| Working | Same | Mahotsav TV | https://livetv.mahotsavtv.com/mahotsavtv/playout/index.m3u8 | https://livetv.mahotsavtv.com/mahotsavtv/playout/index.m3u8 |
| Non-working | Same | Mangalmay TV | https://yupplivegcpusa.yuppcdn.net/100823/mangalmay_1800/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yupplivegcpusa.yuppcdn.net/100823/mangalmay_1800/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | Mercy TV (India) | https://5dd3981940faa.streamlock.net/mercytv/mercytv/playlist.m3u8 | https://5dd3981940faa.streamlock.net/mercytv/mercytv/playlist.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Religious",MH One Shraddha | https://fta.ektv.in/live/344/master.m3u8 | https://fta.ektv.in/live/344/master.m3u8 |
| Working | Same | MTA2 Europe | https://chlivemta1.akamaized.net/hls/live/2008145/mta2/playlist.m3u8 | https://chlivemta1.akamaized.net/hls/live/2008145/mta2/playlist.m3u8 |
| Working | Same | MTA7 Asia | https://livemtaasia.akamaized.net/hls/live/2039224/mtaasia2/playlist.m3u8 | https://livemtaasia.akamaized.net/hls/live/2039224/mtaasia2/playlist.m3u8 |
| Working | Same | Padharo SA | https://samitaorigin.tangotv.in/PADHAROSA/SAMITAORIGIN/index.m3u8 | https://samitaorigin.tangotv.in/PADHAROSA/SAMITAORIGIN/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Religious",Paras Gold | https://fta.ektv.in/live/167/master.m3u8 | https://fta.ektv.in/live/167/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Religious",Peace of Mind TV | https://fta.ektv.in/live/170/master.m3u8 | https://fta.ektv.in/live/170/master.m3u8 |
| Working | Same | Sadhna | https://6n3yow8pl9ok-hls-live.5centscdn.com/sadhanalivetv/live.stream/playlist.m3u8 | https://6n3yow8pl9ok-hls-live.5centscdn.com/sadhanalivetv/live.stream/playlist.m3u8 |
| Working | Same | Sadhna TV | https://mumt05.tangotv.in/87NeALx2SADHNATV/index.m3u8 | https://mumt05.tangotv.in/87NeALx2SADHNATV/index.m3u8 |
| Working | Same | Sanskar TV | https://d26idhjf0y1p2g.cloudfront.net/out/v1/cd66dd25b9774cb29943bab54bbf3e2f/index.m3u8 | https://d26idhjf0y1p2g.cloudfront.net/out/v1/cd66dd25b9774cb29943bab54bbf3e2f/index.m3u8 |
| Working | Same | Sanskar UK | https://d34z4embz0hjf6.cloudfront.net/out/v1/7ac2789ff9a544a49337d1ffc54ce61c/index.m3u8 | https://d34z4embz0hjf6.cloudfront.net/out/v1/7ac2789ff9a544a49337d1ffc54ce61c/index.m3u8 |
| Working | Same | Sanskar USA | https://d2netiedy8cz3x.cloudfront.net/out/v1/9bf6fa4ac8d6432cb98da13b121ba3c2/index.m3u8 | https://d2netiedy8cz3x.cloudfront.net/out/v1/9bf6fa4ac8d6432cb98da13b121ba3c2/index.m3u8 |
| Working | Same | Sanskar Web TV | https://deatfcv3xdvi3.cloudfront.net/out/v1/7a43dd2f64e34ec28da1b4bd6923251a/index.m3u8 | https://deatfcv3xdvi3.cloudfront.net/out/v1/7a43dd2f64e34ec28da1b4bd6923251a/index.m3u8 |
| Working | Same | Satsang TV | https://d2vfwvjxwtwq1t.cloudfront.net/out/v1/6b24239d5517495b986e7705490c6e65/index.m3u8 | https://d2vfwvjxwtwq1t.cloudfront.net/out/v1/6b24239d5517495b986e7705490c6e65/index.m3u8 |
| Working | Same | Satsang Web TV | https://d1ji7e9jbzm5g8.cloudfront.net/out/v1/769f22f64d80442889306b9c4abea63c/index.m3u8 | https://d1ji7e9jbzm5g8.cloudfront.net/out/v1/769f22f64d80442889306b9c4abea63c/index.m3u8 |
| Working | Same | Shubhsandesh TV | https://cdn.pishow.tv/ott/live/457/master.m3u8 | https://cdn.pishow.tv/ott/live/457/master.m3u8 |
| Working | Same | Sindh TV (India) | https://samitaorigin.tangotv.in/SINDHTV/SAMITAORIGIN/index.m3u8 | https://samitaorigin.tangotv.in/SINDHTV/SAMITAORIGIN/index.m3u8 |
| Non-working | Same | Soham TV | https://mumt03.tangotv.in/Dsly5z3HSOHAMTV/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HSOHAMTV/index.m3u8 |
| Working | Same | SVBC 4 | https://player.mslivestream.net/mslive/13a2927187b9700ae7ea82d7841d5b68.sdp/playlist.m3u8 | https://player.mslivestream.net/mslive/13a2927187b9700ae7ea82d7841d5b68.sdp/playlist.m3u8 |
| Working | Same | Swastik TV | https://server.playontv.in/swastiktv/index.m3u8 | https://server.playontv.in/swastiktv/index.m3u8 |
| Working | Same | Total Bhakti | https://d34z4embz0hjf6.cloudfront.net/out/v1/d55b3323a9f142638f897378f0b526fe/index.m3u8 | https://d34z4embz0hjf6.cloudfront.net/out/v1/d55b3323a9f142638f897378f0b526fe/index.m3u8 |
| Working | Same | Vedic | https://d2lk5u59tns74c.cloudfront.net/out/v1/5812b1a12b62482f83c38f9c8d34cb5a/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/5812b1a12b62482f83c38f9c8d34cb5a/index.m3u8 |

## Entertainment

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | Alright! TV | https://d3c7vdfq3tyeyw.cloudfront.net/v1/master/071c0467fcd02420cdf0d8a1ca3524b96c27a151/rusk_media/v1/channel/ruskmedia/germane.m3u8 | https://d3c7vdfq3tyeyw.cloudfront.net/v1/master/071c0467fcd02420cdf0d8a1ca3524b96c27a151/rusk_media/v1/channel/ruskmedia/germane.m3u8 |
| Working | Same | Anjan TV | https://anjan.vstream.online/anjanorg/ngrp:anjan_hdall/playlist.m3u8 | https://anjan.vstream.online/anjanorg/ngrp:anjan_hdall/playlist.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment",Anmol TV | https://fta.ektv.in/live/256/master.m3u8 | https://fta.ektv.in/live/256/master.m3u8 |
| Working | Same | Apna Punjab TV | https://plus.gigabitcdn.net/live-stream/apna-punjab-H3sE/playlist.m3u8 | https://plus.gigabitcdn.net/live-stream/apna-punjab-H3sE/playlist.m3u8 |
| Non-working | Same | Aryan TV National | https://mumt04.tangotv.in/m18aqlK4ARYANTVNATIONAL/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4ARYANTVNATIONAL/index.m3u8 |
| Working | Same | BVG | https://mumt05.tangotv.in/87NeALx2BVG/index.m3u8 | https://mumt05.tangotv.in/87NeALx2BVG/index.m3u8 |
| Working | Same | Colors | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/sg/YuppTV/ColorsAPAC.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/sg/YuppTV/ColorsAPAC.m3u8 |
| Non-working | Same | Colors HD | http://103.135.253.32:8080/Color-HD/index.m3u8 | http://103.135.253.32:8080/Color-HD/index.m3u8 |
| Working | Same | Colors MENA HD | https://da86m1sqpm3o0.cloudfront.net/28072023/smil:colorsme.smil/playlist.m3u8 | https://da86m1sqpm3o0.cloudfront.net/28072023/smil:colorsme.smil/playlist.m3u8 |
| Working | Same | Colors Rishtey | http://163.61.226.31:9981/stream/channelid/297962113?profile=pass | http://163.61.226.31:9981/stream/channelid/297962113?profile=pass |
| Working | Same | Colors Rishtey Americas | https://manatv.akamaized.net/090823/smil:ristheyamerica.smil/playlist.m3u8 | https://manatv.akamaized.net/090823/smil:ristheyamerica.smil/playlist.m3u8 |
| Working | Same | Dangal 2 | https://live-dangal2.akamaized.net/liveabr/playlist.m3u8 | https://live-dangal2.akamaized.net/liveabr/playlist.m3u8 |
| Working | Same | Dangal TV | https://live-dangal.akamaized.net/liveabr/playlist.m3u8 | https://live-dangal.akamaized.net/liveabr/playlist.m3u8 |
| Working | Same | DD Arun Prabha | https://cdn.pishow.tv/ott/live/32/master.m3u8 | https://cdn.pishow.tv/ott/live/32/master.m3u8 |
| Working | Same | DD Bharati | https://cdn.pishow.tv/ott/live/10/master.m3u8 | https://cdn.pishow.tv/ott/live/10/master.m3u8 |
| Working | Same | DD Bihar | https://cdn.pishow.tv/ott/live/35/master.m3u8 | https://cdn.pishow.tv/ott/live/35/master.m3u8 |
| Working | Same | DD Chhattisgarh | https://cdn.pishow.tv/ott/live/15/master.m3u8 | https://cdn.pishow.tv/ott/live/15/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="General",DD Haryana | https://fta.ektv.in/live/580/master.m3u8 | https://fta.ektv.in/live/580/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="General",DD Himachal Pradesh | https://fta.ektv.in/live/575/master.m3u8 | https://fta.ektv.in/live/575/master.m3u8 |
| Working | Same | DD Jharkhand | https://cdn.pishow.tv/ott/live/1617/master.m3u8 | https://cdn.pishow.tv/ott/live/1617/master.m3u8 |
| Working | Same | DD Kashir | https://cdn.pishow.tv/ott/live/16/master.m3u8 | https://cdn.pishow.tv/ott/live/16/master.m3u8 |
| Working | Same | DD Kisan | https://mumbai-edge.smartplaytv.in/DDKisan/index.m3u8 | https://mumbai-edge.smartplaytv.in/DDKisan/index.m3u8 |
| Working | Same | DD Madhya Pradesh | https://mumbai-edge.smartplaytv.in/ddmadhyapradesh/index.m3u8 | https://mumbai-edge.smartplaytv.in/ddmadhyapradesh/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="General",DD Manipur | https://fta.ektv.in/live/671/master.m3u8 | https://fta.ektv.in/live/671/master.m3u8 |
| Working | Same | DD National | http://163.61.226.31:9981/stream/channelid/1991369999?profile=pass | http://163.61.226.31:9981/stream/channelid/1991369999?profile=pass |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment",DD National HD | https://fta.ektv.in/live/15/master.m3u8 | https://fta.ektv.in/live/15/master.m3u8 |
| Working | Same | DD Rajasthan | https://cdn.pishow.tv/ott/live/34/master.m3u8 | https://cdn.pishow.tv/ott/live/34/master.m3u8 |
| Working | Same | DD Uttar Pradesh | https://cdn.pishow.tv/ott/live/36/master.m3u8 | https://cdn.pishow.tv/ott/live/36/master.m3u8 |
| Working | Same | DD Uttarakhand | https://cdn.pishow.tv/ott/live/17/master.m3u8 | https://cdn.pishow.tv/ott/live/17/master.m3u8 |
| Working | Same | Disha TV | https://d1msejlow1t3l4.cloudfront.net/fta/dishatv/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/dishatv/playlist.m3u8 |
| Working | Same | Diya TV | https://stream.diyatvinc.com/diya.m3u8 | https://stream.diyatvinc.com/diya.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment",E 24 | https://fta.ektv.in/live/159/master.m3u8 | https://fta.ektv.in/live/159/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment",Epic Bharat | https://fta.ektv.in/live/471/master.m3u8 | https://fta.ektv.in/live/471/master.m3u8 |
| Working | Same | Epic Bharat Digital | https://cc-p1izg43bk7sj5.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-p1izg43bk7sj5/DIYC/PMSL/IN10/Nazara_IN_B/Nazara_IN_B.m3u8 | https://cc-p1izg43bk7sj5.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-p1izg43bk7sj5/DIYC/PMSL/IN10/Nazara_IN_B/Nazara_IN_B.m3u8 |
| Working | Same | Epic Crimes | https://cc-wsuyg2uxeak04.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-wsuyg2uxeak04/master.m3u8 | https://cc-wsuyg2uxeak04.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-wsuyg2uxeak04/master.m3u8 |
| Working | Same | Epic TV Digital | https://cc-czbq30x55knit.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-czbq30x55knit/DIYC/PMSL/IN10/Epic_TV_IN_B/Epic_TV_IN_B.m3u8 | https://cc-czbq30x55knit.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-czbq30x55knit/DIYC/PMSL/IN10/Epic_TV_IN_B/Epic_TV_IN_B.m3u8 |
| Working | Same | Gangaur TV | https://pbgangaur.wiseplayout.com/Gangaur/master.m3u8 | https://pbgangaur.wiseplayout.com/Gangaur/master.m3u8 |
| Working | Same | Gyandarshan | https://cdn.pishow.tv/ott/live/14/master.m3u8 | https://cdn.pishow.tv/ott/live/14/master.m3u8 |
| Working | Same | Gyandarshan HD | https://mumt05.tangotv.in/87NeALx2GYANDARSHAN/index.m3u8 | https://mumt05.tangotv.in/87NeALx2GYANDARSHAN/index.m3u8 |
| Working | Same | HSTV | https://live.castmaxcloud.com/live/hstv.m3u8 | https://live.castmaxcloud.com/live/hstv.m3u8 |
| Working | Same | Hyder TV | https://cdn.live247stream.com/hyder/tv/playlist.m3u8 | https://cdn.live247stream.com/hyder/tv/playlist.m3u8 |
| Working | Same | Jan TV | https://d1msejlow1t3l4.cloudfront.net/fta/jantv/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/jantv/playlist.m3u8 |
| Non-working | Same | Jus Hindi | http://103.154.3.101:5001/live/960.m3u8 | http://103.154.3.101:5001/live/960.m3u8 |
| Non-working | Same | Jus One | http://103.154.3.101:5001/live/961.m3u8 | http://103.154.3.101:5001/live/961.m3u8 |
| Working | Same | Kaumudy TV | https://oqgdrkxby4rm-hls-live.5centscdn.com/kaumudytv/live.stream/playlist.m3u8 | https://oqgdrkxby4rm-hls-live.5centscdn.com/kaumudytv/live.stream/playlist.m3u8 |
| Working | Same | Mango (India) | https://stmv6.voxtvhd.com.br/cinehindi/cinehindi/playlist.m3u8 | https://stmv6.voxtvhd.com.br/cinehindi/cinehindi/playlist.m3u8 |
| Working | Same | Manoranjan TV | https://cdn.pishow.tv/ott/live/1013/master.m3u8 | https://cdn.pishow.tv/ott/live/1013/master.m3u8 |
| Working | Same | Mh 1 Prime | https://mumt04.tangotv.in/m18aqlK4MHONE/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4MHONE/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment",MH One Dil Se | https://fta.ektv.in/live/351/master.m3u8 | https://fta.ektv.in/live/351/master.m3u8 |
| Working | Same | Network 10 | https://mumbai-edge.smartplaytv.in/Network10/index.m3u8 | https://mumbai-edge.smartplaytv.in/Network10/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Undefined",Prarthana Bhawan TV | https://fta.ektv.in/live/623/master.m3u8 | https://fta.ektv.in/live/623/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment",Q TV | https://fta.ektv.in/live/25/master.m3u8 | https://fta.ektv.in/live/25/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Undefined",Raftaar Media | https://fta.ektv.in/live/306/master.m3u8 | https://fta.ektv.in/live/306/master.m3u8 |
| Working | Same | Rongeen TV | https://server.thelegitpro.in/rongeentv/rongeentv/index.m3u8 | https://server.thelegitpro.in/rongeentv/rongeentv/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Undefined",Saam TV | https://fta.ektv.in/live/650/master.m3u8 | https://fta.ektv.in/live/650/master.m3u8 |
| Working | Same | Sansad TV 1 | https://playhls.media.nic.in/hls/live/lstv/lstv.m3u8 | https://playhls.media.nic.in/hls/live/lstv/lstv.m3u8 |
| Working | Same | Sansad TV 1 HD | https://d2lk5u59tns74c.cloudfront.net/out/v1/fff8f20221d5456e8922e689d71dedc3/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/fff8f20221d5456e8922e689d71dedc3/index.m3u8 |
| Working | Same | Sansad TV 2 | https://cdn.pishow.tv/ott/live/39/master.m3u8 | https://cdn.pishow.tv/ott/live/39/master.m3u8 |
| Working | Same | Sansad TV 2 HD | https://d2lk5u59tns74c.cloudfront.net/out/v1/e4182054dce340da9e0ff38b6b3658a4/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/e4182054dce340da9e0ff38b6b3658a4/index.m3u8 |
| Working | Same | Santvani Channel | https://d1hyhsds9hb4o2.cloudfront.net/master.m3u8 | https://d1hyhsds9hb4o2.cloudfront.net/master.m3u8 |
| Working | Same | Sarv Dharm Sangam | https://d1msejlow1t3l4.cloudfront.net/fta/sarvdharmsangam/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/sarvdharmsangam/playlist.m3u8 |
| Working | Same | Sharnam TV | https://d1msejlow1t3l4.cloudfront.net/fta/sharanamtv/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/sharanamtv/playlist.m3u8 |
| Working | Same | Shemaroo TV | https://airtelapp.shemaroo.com/shemarootv/smil:shemarootvadp.smil/playlist.m3u8 | https://airtelapp.shemaroo.com/shemarootv/smil:shemarootvadp.smil/playlist.m3u8 |
| Working | Same | Shemaroo Umang | https://airtelapp.shemaroo.com/shemarooumang/smil:shemarooumangadp.smil/playlist.m3u8 | https://airtelapp.shemaroo.com/shemarooumang/smil:shemarooumangadp.smil/playlist.m3u8 |
| Working | Same | Shubh TV | https://d2g1vdc6ozl2o8.cloudfront.net/out/v1/0a0dc7d7911b4fddbb4dfc963fdd4b9e/index.m3u8 | https://d2g1vdc6ozl2o8.cloudfront.net/out/v1/0a0dc7d7911b4fddbb4dfc963fdd4b9e/index.m3u8 |
| Working | Same | Sony Entertainment Television HD | http://38.96.178.205/SONYHD/index.m3u8 | http://38.96.178.205/SONYHD/index.m3u8 |
| Working | Same | Sony KAL Hindi | https://wurlsonypicturestv.global.transmit.live/hls/68deeb1c0238cda82df543dd/v1/spt_sonykal_1/lg_us/latest/main/hls/playlist.m3u8 | https://wurlsonypicturestv.global.transmit.live/hls/68deeb1c0238cda82df543dd/v1/spt_sonykal_1/lg_us/latest/main/hls/playlist.m3u8 |
| Non-working | Same | Sony Pal | http://59.103.38.46:8000/play/a0ac/index.m3u8 | http://59.103.38.46:8000/play/a0ac/index.m3u8 |
| Working | Same | SRK TV | https://srknowapp.ncare.live/srktvhlswodrm/srktv.stream/playlist.m3u8 | https://srknowapp.ncare.live/srktvhlswodrm/srktv.stream/playlist.m3u8 |
| Working | Same | Star Bharat (United Kingdom) | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/gb/YuppTV/UtsavBharat.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/gb/YuppTV/UtsavBharat.m3u8 |
| Working | Same | Star Utsav | http://163.61.226.31:9981/stream/channelid/894286890?profile=pass | http://163.61.226.31:9981/stream/channelid/894286890?profile=pass |
| Non-working | Same | StarPlus (India) HD | http://66.102.126.10:8000/play/a008/index.m3u8 | http://66.102.126.10:8000/play/a008/index.m3u8 |
| Working | Same | StarPlus (United Kingdom) | https://d1rc86nwwc9fag.cloudfront.net/260723/starplusuk_2500/chunks.m3u8 | https://d1rc86nwwc9fag.cloudfront.net/260723/starplusuk_2500/chunks.m3u8 |
| Working | Same | Swastik Stories | https://amg14122-amg14122c1-amgplt0835.playout.now3.amagi.tv/playout/amg14122/amg14122c1/amgplt0835/amgplt0835.m3u8 | https://amg14122-amg14122c1-amgplt0835.playout.now3.amagi.tv/playout/amg14122/amg14122c1/amgplt0835/amgplt0835.m3u8 |
| Working | Same | Taaza TV | https://live.we2live.in/taazatv/live/playlist.m3u8 | https://live.we2live.in/taazatv/live/playlist.m3u8 |
| Working | Same | TAG TV (1080p) | http://cdn11.live247stream.com/tag/tv/playlist.m3u8 | http://cdn11.live247stream.com/tag/tv/playlist.m3u8 |
| Working | Same | Tehzeeb TV | https://cdn.pishow.tv/ott/live/239/master.m3u8 | https://cdn.pishow.tv/ott/live/239/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Undefined",The Q India | http://103.175.73.12:8080/live/25/25_0.m3u8 | http://103.175.73.12:8080/live/25/25_0.m3u8 |
| Working | Same | Total TV Haryana | https://d2lk5u59tns74c.cloudfront.net/out/v1/4836fb71b5764f70ab1f3815e0295dfd/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/4836fb71b5764f70ab1f3815e0295dfd/index.m3u8 |
| Working | Same | Trishul Broadcasting Network (720p) | https://live.suricloud.com/hls/tbntv/index.m3u8 | https://live.suricloud.com/hls/tbntv/index.m3u8 |
| Working | Same | TV2 (Malaysia) | https://d25tgymtnqzu8s.cloudfront.net/smil:tv2/playlist.m3u8?id=2 | https://d25tgymtnqzu8s.cloudfront.net/smil:tv2/playlist.m3u8?id=2 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Undefined",TV 100 (India) | https://fta.ektv.in/live/310/master.m3u8 | https://fta.ektv.in/live/310/master.m3u8 |
| Working | Same | Utsav Bharat | https://d1taaads3ztvmu.cloudfront.net/120723/smil:lifeokuk.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://d1taaads3ztvmu.cloudfront.net/120723/smil:lifeokuk.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | Utsav Plus | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/gb/YuppTV/UtsavPlus.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/gb/YuppTV/UtsavPlus.m3u8 |
| Non-working | Same | VTU | https://lbgo.bozztv.com/ssh101/ssh101/afghantheatretv/playlist.m3u8 | https://lbgo.bozztv.com/ssh101/ssh101/afghantheatretv/playlist.m3u8 |
| Working | Same | WeatherSpy (India) | https://jukin-weatherspy-2-in.samsung.wurl.tv/playlist.m3u8 | https://jukin-weatherspy-2-in.samsung.wurl.tv/playlist.m3u8 |
| Non-working | Same | Zee Comedy Nation | https://amg00862-amg00862c5-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c5-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c5-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c5-amgplt0173/playlist.m3u8 |
| Non-working | Same | Zee Dil Se | https://amg00862-amg00862c6-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c6-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c6-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c6-amgplt0173/playlist.m3u8 |
| Non-working | Same | Zee Horror Nights | https://amg00862-amg00862c7-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c7-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c7-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c7-amgplt0173/playlist.m3u8 |
| Non-working | Same | Zee TV HD | http://103.135.253.32:8080/ZEE-TV/index.m3u8 | http://103.135.253.32:8080/ZEE-TV/index.m3u8 |
| Working | Same | Zingabad | https://stream.ottlive.co.in/zingabad/index.m3u8 | https://stream.ottlive.co.in/zingabad/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment",Captain | https://fta.ektv.in/live/173/master.m3u8 | https://fta.ektv.in/live/173/master.m3u8 |
| Working | Same | Manoranjan Prime | https://cdn.pishow.tv/ott/live/1474/master.m3u8 | https://cdn.pishow.tv/ott/live/1474/master.m3u8 |
| Working | Same | Pasand TV | https://d1msejlow1t3l4.cloudfront.net/fta/pasand/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/pasand/playlist.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="General",DD India | https://fta.ektv.in/live/119/119_0.m3u8 | https://fta.ektv.in/live/119/119_0.m3u8 |

## Lifestyle

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | Food Food | https://d2lk5u59tns74c.cloudfront.net/out/v1/ffc601b3dc8d41c5b09115702538d75a/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/ffc601b3dc8d41c5b09115702538d75a/index.m3u8 |
| Non-working | Same | Foodxp | https://techtraveleat.in/stream.m3u8?id=foodxp | https://techtraveleat.in/stream.m3u8?id=foodxp |
| Non-working | Same | Travelxp 4K HDR (2160p) | https://deltatesttatasky.akamaized.net/out/i/968284.m3u8 | https://deltatesttatasky.akamaized.net/out/i/968284.m3u8 |
| Working | Same | Travelxp HD (1080p) | https://amg00416-amg00416c9-samsung-in-4882.playouts.now.amagi.tv/playlist/amg00416-travelxp-travelxphd-samsungin/playlist.m3u8 | https://amg00416-amg00416c9-samsung-in-4882.playouts.now.amagi.tv/playlist/amg00416-travelxp-travelxphd-samsungin/playlist.m3u8 |

## Movie

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Non-working | Same | &TV International | https://amg01117-amg01117c1-amgplt0029.playout.now3.amagi.tv/playlist/amg01117-amg01117c1-amgplt0029/playlist.m3u8 | https://amg01117-amg01117c1-amgplt0029.playout.now3.amagi.tv/playlist/amg01117-amg01117c1-amgplt0029/playlist.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Movies",All Time Movies | https://fta.ektv.in/live/54/54_0.m3u8 | https://fta.ektv.in/live/54/54_0.m3u8 |
| Working | Same | B4U Kadak | https://amg00877-b4unew-amg00877c4-xiaomi-in-5473.playouts.now.amagi.tv/playlist.m3u8 | https://amg00877-b4unew-amg00877c4-xiaomi-in-5473.playouts.now.amagi.tv/playlist.m3u8 |
| Working | Same | B4U Movies | https://amg00877-b4unew-amg00877c2-xiaomi-in-5489.playouts.now.amagi.tv/playlist.m3u8 | https://amg00877-b4unew-amg00877c2-xiaomi-in-5489.playouts.now.amagi.tv/playlist.m3u8 |
| Working | Same | Bollygold | https://jmp2.uk/stvp-IN4000600Q | https://jmp2.uk/stvp-IN4000600Q |
| Working | Same | Bollywood Classic Romania | https://hls02ns.antenaplay.ro/hls/bollywood-sd/index.m3u8 | https://hls02ns.antenaplay.ro/hls/bollywood-sd/index.m3u8 |
| Working | Same | Bollywood HD Russia | https://xykt-fix.github.io/cinerama_edge01/hls/BOLLYWOOD_RU/Movie009.m3u8 | https://xykt-fix.github.io/cinerama_edge01/hls/BOLLYWOOD_RU/Movie009.m3u8 |
| Working | Same | Colors Cineplex | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/gb/YuppTV/ColorsCineplexUK.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/gb/YuppTV/ColorsCineplexUK.m3u8 |
| Working | Same | Colors Cineplex Bollywood | http://163.61.226.31:9981/stream/channelid/1709941389?profile=pass | http://163.61.226.31:9981/stream/channelid/1709941389?profile=pass |
| Working | Same | Colors Cineplex Superhits | http://163.61.226.31:9981/stream/channelid/2039746374?profile=pass | http://163.61.226.31:9981/stream/channelid/2039746374?profile=pass |
| Non-working | Same | Goldmines 2 | https://mumt03.tangotv.in/Dsly5z3HGOLDMINES2/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HGOLDMINES2/index.m3u8 |
| Working | Same | Goldmines | https://mumt04.tangotv.in/m18aqlK4GOLDMINES/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4GOLDMINES/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Movies",Goldmines Action | https://fta.ektv.in/live/584/master.m3u8 | https://fta.ektv.in/live/584/master.m3u8 |
| Non-working | Same | Goldmines Bollywood | https://mumt03.tangotv.in/Dsly5z3HGOLDMINESBOLLYWOOD/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HGOLDMINESBOLLYWOOD/index.m3u8 |
| Working | Same | Goldmines Movies | https://mumt04.tangotv.in/m18aqlK4GOLDMINEMOVIES/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4GOLDMINEMOVIES/index.m3u8 |
| Working | Same | India Talkies | https://samitaorigin.tangotv.in/INDIATALKIES/SAMITAORIGIN/index.m3u8 | https://samitaorigin.tangotv.in/INDIATALKIES/SAMITAORIGIN/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Movies",Maha Movie | https://fta.ektv.in/live/48/48_0.m3u8 | https://fta.ektv.in/live/48/48_0.m3u8 |
| Working | Same | Manoranjan Grand | https://cdn.pishow.tv/ott/live/1011/master.m3u8 | https://cdn.pishow.tv/ott/live/1011/master.m3u8 |
| Working | Same | MBC Bollywood (1080p) | https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-bollywood/546eb40d7dcf9a209255dd2496903764/index.m3u8 | https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-bollywood/546eb40d7dcf9a209255dd2496903764/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Movies",MH One Movies | https://fta.ektv.in/live/639/master.m3u8 | https://fta.ektv.in/live/639/master.m3u8 |
| Working | Same | NH BollyFlix | https://jmp2.uk/stvp-IN46000140Q | https://jmp2.uk/stvp-IN46000140Q |
| Non-working | Same | Pocket Films | https://vglivessai.akamaized.net/sg/v1/manifest/611d79b11b77e2f571934fd80ca1413453772ac7/b8ada260-bb81-472b-b7c1-3a79213a84b8/e02a0ce5-6c42-4cca-bb53-e5cfecff74a9/0.m3u8 | https://vglivessai.akamaized.net/sg/v1/manifest/611d79b11b77e2f571934fd80ca1413453772ac7/b8ada260-bb81-472b-b7c1-3a79213a84b8/e02a0ce5-6c42-4cca-bb53-e5cfecff74a9/0.m3u8 |
| Non-working | Same | Shemaroo Filmi Gaane | https://prod-runn.cdn.runn.tv/shemaroo/stream/smrfgn/playlist.m3u8 | https://prod-runn.cdn.runn.tv/shemaroo/stream/smrfgn/playlist.m3u8 |
| Working | Same | Shemaroo Josh | https://cdn.pishow.tv/ott/live/337/master.m3u8 | https://cdn.pishow.tv/ott/live/337/master.m3u8 |
| Working | Same | Shubh Cinema TV | https://d393sxaxig6bax.cloudfront.net/out/v1/589cf2cf44bf42bb941e817a2240d62e/index.m3u8 | https://d393sxaxig6bax.cloudfront.net/out/v1/589cf2cf44bf42bb941e817a2240d62e/index.m3u8 |
| Working | Same | Sony Wah | http://163.61.226.31:9981/stream/channelid/1743466790?profile=pass | http://163.61.226.31:9981/stream/channelid/1743466790?profile=pass |
| Working | Same | South Station | https://cc-yw7ztecy8do3q.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-yw7ztecy8do3q/SS_IN.m3u8 | https://cc-yw7ztecy8do3q.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-yw7ztecy8do3q/SS_IN.m3u8 |
| Working | Same | Star Utsav Movies | http://163.61.226.31:9981/stream/channelid/1225596390?profile=pass | http://163.61.226.31:9981/stream/channelid/1225596390?profile=pass |
| Working | Same | The Movie Club | https://mumbai-edge.smartplaytv.in/TheMovieClub/index.m3u8 | https://mumbai-edge.smartplaytv.in/TheMovieClub/index.m3u8 |
| Working | Same | The Movie Club +2 | https://d3gnyty2vddhsg.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/pb-ytipwjqub3kf8/TMC2_IN.m3u8?ads.ads_cdn=cf&ads.cdn=cf | https://d3gnyty2vddhsg.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/pb-ytipwjqub3kf8/TMC2_IN.m3u8?ads.ads_cdn=cf&ads.cdn=cf |
| Non-working | Same | Zee Cine Classic | https://amg00862-amg00862c8-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c8-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c8-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c8-amgplt0173/playlist.m3u8 |
| Working | Same | Zee Cinema APAC | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/sg/YuppTV/ZeeCinemaAPAC.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/sg/YuppTV/ZeeCinemaAPAC.m3u8 |
| Non-working | Same | Zee South Flix | https://amg00862-amg00862c9-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c9-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c9-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c9-amgplt0173/playlist.m3u8 |
| Working | Same | B4U Bhojpuri | https://cdnb4u.wiseplayout.com/B4U_Bhojpuri/master.m3u8 | https://cdnb4u.wiseplayout.com/B4U_Bhojpuri/master.m3u8 |
| Working | Same | B4U Bhojpuri Plus | https://cc-t2mudtkmuz4wb.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-t2mudtkmuz4wb/B4U_Bhojpuri/master.m3u8 | https://cc-t2mudtkmuz4wb.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-t2mudtkmuz4wb/B4U_Bhojpuri/master.m3u8 |
| Working | Same | Bhojpuri Cinema | https://live-bhojpuri.akamaized.net/liveabr/playlist.m3u8 | https://live-bhojpuri.akamaized.net/liveabr/playlist.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Movies",Epic Bhojpuri | https://fta.ektv.in/live/467/master.m3u8 | https://fta.ektv.in/live/467/master.m3u8 |
| Working | Same | Epic Bhojpuri Digital | https://cc-8hy4a26pz2uos.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-8hy4a26pz2uos/playlist.m3u8 | https://cc-8hy4a26pz2uos.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-8hy4a26pz2uos/playlist.m3u8 |
| Working | Same | Mahua Play | https://cdn.ottlive.co.in/mahuaplay/index.m3u8 | https://cdn.ottlive.co.in/mahuaplay/index.m3u8 |
| Working | Same | Oscar Movies Bhojpuri | https://cdn.pishow.tv/ott/live/233/master.m3u8 | https://cdn.pishow.tv/ott/live/233/master.m3u8 |

## Music

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | 7X Music | https://7xshreeshyam.akamaized.net/7XPunjabi/index.m3u8 | https://7xshreeshyam.akamaized.net/7XPunjabi/index.m3u8 |
| Working | Same | 9X Jalwa | https://wiselp.wiseplayout.com/9X_Jalwa/master.m3u8 | https://wiselp.wiseplayout.com/9X_Jalwa/master.m3u8 |
| Non-working | Same | 9XM | https://9xjio.wiseplayout.com/9XM/master.m3u8 | https://9xjio.wiseplayout.com/9XM/master.m3u8 |
| Non-working | Same | Andy Haryana | https://mumt03.tangotv.in/Dsly5z3HANDYHARYANA/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HANDYHARYANA/index.m3u8 |
| Working | Same | B4U Music | https://amg00877-b4unew-amg00877c3-xiaomi-in-5474.playouts.now.amagi.tv/720p/index.m3u8 | https://amg00877-b4unew-amg00877c3-xiaomi-in-5474.playouts.now.amagi.tv/720p/index.m3u8 |
| Working | Same | Balle Balle | https://mcncdndigital.com/worldpunjabitv/index.m3u8 | https://mcncdndigital.com/worldpunjabitv/index.m3u8 |
| Working | Same | Balle Balle HD | https://mcncdndigital.com/balleballetv/index.m3u8 | https://mcncdndigital.com/balleballetv/index.m3u8 |
| Working | Same | Boogle Bollywood | https://yuppnimrestreammum.akamaized.net/181224/smil:bogglebollywood.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yuppnimrestreammum.akamaized.net/181224/smil:bogglebollywood.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Non-working | Same | Deewana HD | https://live20.bozztv.com/giatvplayout7/giatv-209592/index.m3u8 | https://live20.bozztv.com/giatvplayout7/giatv-209592/index.m3u8 |
| Non-working | Same | Dhamaal (576p) | https://tvsen6.aynaott.com/F4Z6es8E/index.m3u8 | https://tvsen6.aynaott.com/F4Z6es8E/index.m3u8 |
| Non-working | Same | Epic Music | http://66.102.126.10:8000/play/a01i/index.m3u8 | http://66.102.126.10:8000/play/a01i/index.m3u8 |
| Working | Same | Epic Music Digital | https://cc-3cyxq80qusspd.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-3cyxq80qusspd/playlist.m3u8 | https://cc-3cyxq80qusspd.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-3cyxq80qusspd/playlist.m3u8 |
| Working | Same | Hindi Hits | http://146.59.253.52:8080/hindihitshd/index.m3u8 | http://146.59.253.52:8080/hindihitshd/index.m3u8 |
| Working | Same | Insync | https://d1msejlow1t3l4.cloudfront.net/fta/insync/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/insync/playlist.m3u8 |
| Working | Same | Mastiii | https://mumbai-edge.smartplaytv.in/MastiMusic/index.m3u8 | https://mumbai-edge.smartplaytv.in/MastiMusic/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/154.0.0.0 Safari/537.36" group-title="Entertainment",MTV (India) | https://yupp-music.keralive.workers.dev/out/v1/a797c00cba954265ba781f92a57e2cf5/index.m3u8 | https://yupp-music.keralive.workers.dev/out/v1/a797c00cba954265ba781f92a57e2cf5/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/130.0.0.0 Safari/537.36" group-title="Entertainment",MTV (India) HD | https://maamusic.keralive.workers.dev/out/v1/a797c00cba954265ba781f92a57e2cf5/index.m3u8 | https://maamusic.keralive.workers.dev/out/v1/a797c00cba954265ba781f92a57e2cf5/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Music",Music India | https://fta.ektv.in/live/158/master.m3u8 | https://fta.ektv.in/live/158/master.m3u8 |
| Working | Same | NH BollyRaga | https://jmp2.uk/stvp-IN460001373 | https://jmp2.uk/stvp-IN460001373 |
| Working | Same | Songdew TV | https://yuppnimrestreammum.akamaized.net/181224/smil:songdewtv.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yuppnimrestreammum.akamaized.net/181224/smil:songdewtv.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | Steelbird Music (720p) | https://cdn2.in/SteelbirdMusicTVhls/live.m3u8 | https://cdn2.in/SteelbirdMusicTVhls/live.m3u8 |
| Working | Same | Vision Beats | http://a-edge.bliscdn.com/Visionbeats/index.m3u8 | http://a-edge.bliscdn.com/Visionbeats/index.m3u8 |
| Working | Same | YRF Music | https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg01412-xiaomiasia-yrfmusic-xiaomi/playlist.m3u8 | https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg01412-xiaomiasia-yrfmusic-xiaomi/playlist.m3u8 |
| Working | Same | YRF Music Nepal | https://vidaa.kableone.com/hls/live/2111218/YrfMusic/1.m3u8 | https://vidaa.kableone.com/hls/live/2111218/YrfMusic/1.m3u8 |
| Working | Same | Zoom (India) | https://dai.google.com/linear/hls/event/JCAm25qkRXiKcK1AJMlvKQ/master.m3u8 | https://dai.google.com/linear/hls/event/JCAm25qkRXiKcK1AJMlvKQ/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Music",Sangeet Bhojpuri | https://fta.ektv.in/live/349/master.m3u8 | https://fta.ektv.in/live/349/master.m3u8 |
| Working | Same | 7S Music | https://cdn.pishow.tv/ott/live/1257/master.m3u8 | https://cdn.pishow.tv/ott/live/1257/master.m3u8 |
| Working | Same | 9X Jhakaas | https://amg01281-9xmediapvtltd-9xjhakaas-samsungin-ci2cs.amagi.tv/playlist/amg01281-9xmediapvtltd-9xjhakaas-samsungin/playlist.m3u8 | https://amg01281-9xmediapvtltd-9xjhakaas-samsungin-ci2cs.amagi.tv/playlist/amg01281-9xmediapvtltd-9xjhakaas-samsungin/playlist.m3u8 |
| Working | Same | 9X Tashan | https://amg01281-9xmediapvtltd-9xtashan-samsungin-xz1sd.amagi.tv/playlist/amg01281-9xmediapvtltd-9xtashan-samsungin/playlist.m3u8 | https://amg01281-9xmediapvtltd-9xtashan-samsungin-xz1sd.amagi.tv/playlist/amg01281-9xmediapvtltd-9xtashan-samsungin/playlist.m3u8 |
| Working | Same | Dhoom Music | https://cdn.pishow.tv/ott/live/1456/master.m3u8 | https://cdn.pishow.tv/ott/live/1456/master.m3u8 |
| Non-working | Same | ETV Music | https://mumbai-edge.smartplaytv.in/ETVABHIRUCHI/index.m3u8 | https://mumbai-edge.smartplaytv.in/ETVABHIRUCHI/index.m3u8 |
| Working | Same | Mh 1 Music | https://livestream.jswk.online/playlisttest/live/playlist.m3u8 | https://livestream.jswk.online/playlisttest/live/playlist.m3u8 |
| Working | Same | PTC Music | https://d2lk5u59tns74c.cloudfront.net/out/v1/f913cf893c594f73b114216e74a2efbc/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/f913cf893c594f73b114216e74a2efbc/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Music",Public Music | https://fta.ektv.in/live/240/master.m3u8 | https://fta.ektv.in/live/240/master.m3u8 |
| Working | Same | Tarang Music | https://livetv.tarangplus.in/tarangmusic-origin/live/playlist.m3u8 | https://livetv.tarangplus.in/tarangmusic-origin/live/playlist.m3u8 |
| Working | Same | ZB Music | https://server.zillarbarta.com/zbmusic/index.m3u8 | https://server.zillarbarta.com/zbmusic/index.m3u8 |

## News

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | 22Scope News | https://thelegitpro.in/HDlive/22scope/index.fmp4.m3u8 | https://thelegitpro.in/HDlive/22scope/index.fmp4.m3u8 |
| Working | Same | Aagaaz Times | https://live1.ottlive.co.in/aagaaztimes/index.m3u8 | https://live1.ottlive.co.in/aagaaztimes/index.m3u8 |
| Working | Same | Aaj Ki Khabar | https://stream.ottlive.co.in/aajkikhabar/index.m3u8 | https://stream.ottlive.co.in/aajkikhabar/index.m3u8 |
| Non-working | Same | Aaj Tak | http://103.213.31.109:90/AajtakHD/playlist.m3u8 | http://103.213.31.109:90/AajtakHD/playlist.m3u8 |
| Working | Same | Aaj Tak HD | https://feeds.intoday.in/aajtak/api/aajtakhd/master.m3u8 | https://feeds.intoday.in/aajtak/api/aajtakhd/master.m3u8 |
| Working | Same | ABP Ganga | https://d2l4ar6y3mrs4k.cloudfront.net/live-streaming/ganga-livetv/master.m3u8 | https://d2l4ar6y3mrs4k.cloudfront.net/live-streaming/ganga-livetv/master.m3u8 |
| Working | Same | ABP News | https://d1rc86nwwc9fag.cloudfront.net/vglive-sk-472500/abpnews/master.m3u8 | https://d1rc86nwwc9fag.cloudfront.net/vglive-sk-472500/abpnews/master.m3u8 |
| Non-working | Same | AmarUjala | https://amarujala.ottlive.co.in/amarujala/index.m3u8 | https://amarujala.ottlive.co.in/amarujala/index.m3u8 |
| Working | Same | ANB News | https://stream.ottlive.co.in/anb/index.m3u8 | https://stream.ottlive.co.in/anb/index.m3u8 |
| Working | Same | APN | https://d1msejlow1t3l4.cloudfront.net/fta/apnnews/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/apnnews/playlist.m3u8 |
| Working | Same | Argus News | https://mumt05.tangotv.in/87NeALx2ARGUSNEWS/index.m3u8 | https://mumt05.tangotv.in/87NeALx2ARGUSNEWS/index.m3u8 |
| Working | Same | Asian News | https://stream.ottlive.co.in/asiannews/index.m3u8 | https://stream.ottlive.co.in/asiannews/index.m3u8 |
| Working | Same | ATN Samachar | https://newsliveindia.com:4433/atn/index.m3u8 | https://newsliveindia.com:4433/atn/index.m3u8 |
| Working | Same | Awaaz India TV (720p) | https://awaazindia.livebox.co.in/AwaazIndaTVhls/Live.m3u8 | https://awaazindia.livebox.co.in/AwaazIndaTVhls/Live.m3u8 |
| Working | Same | Bansal News | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/4f8d92312b9a4783bbd706cf7ed86085/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/4f8d92312b9a4783bbd706cf7ed86085/index.m3u8 |
| Working | Same | Bharat24 | https://vglivessai.akamaized.net/ptnr-lg/title-Bharat24News_LGIndia/sg/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/ebcf5152-686a-43ae-ad13-15bc198112b7/index.m3u8 | https://vglivessai.akamaized.net/ptnr-lg/title-Bharat24News_LGIndia/sg/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/ebcf5152-686a-43ae-ad13-15bc198112b7/index.m3u8 |
| Working | Same | Bharat AtoZ | https://live.ekamraott.com/4tv/bharata2z/index.m3u8 | https://live.ekamraott.com/4tv/bharata2z/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",Bharat Samachar | https://fta.ektv.in/live/97/97_0.m3u8 | https://fta.ektv.in/live/97/97_0.m3u8 |
| Working | Same | BSTV (India) | https://samitaorigin.tangotv.in/BSTV/SAMITAORIGIN/index.m3u8 | https://samitaorigin.tangotv.in/BSTV/SAMITAORIGIN/index.m3u8 |
| Working | Same | Cnews Bharat | https://legitpro.co.in/cnews/cnews/index.fmp4.m3u8 | https://legitpro.co.in/cnews/cnews/index.fmp4.m3u8 |
| Working | Same | DD News | https://mumbai-edge.smartplaytv.in/DDNews/index.m3u8 | https://mumbai-edge.smartplaytv.in/DDNews/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",DD News HD | https://fta.ektv.in/live/117/117_0.m3u8 | https://fta.ektv.in/live/117/117_0.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",DNN | https://fta.ektv.in/live/592/master.m3u8 | https://fta.ektv.in/live/592/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",First India News | https://fta.ektv.in/live/596/master.m3u8 | https://fta.ektv.in/live/596/master.m3u8 |
| Working | Same | Global India | https://server.livelegitpro.in/globalindiatv/globalindiatv/video.m3u8 | https://server.livelegitpro.in/globalindiatv/globalindiatv/video.m3u8 |
| Working | Same | Good News Today | https://d2lk5u59tns74c.cloudfront.net/out/v1/75f3183e143240a29fbddd502a6a3f8d/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/75f3183e143240a29fbddd502a6a3f8d/index.m3u8 |
| Working | Same | Har Khabar | https://samitaorigin.tangotv.in/HARKHABAR/SAMITAORIGIN/index.m3u8 | https://samitaorigin.tangotv.in/HARKHABAR/SAMITAORIGIN/index.m3u8 |
| Working | Same | Hindi Khabar | https://stream.ottlive.co.in/hindikhabar/index.m3u8 | https://stream.ottlive.co.in/hindikhabar/index.m3u8 |
| Working | Same | HNN 24x7 | https://ott.livelegitpro.in:9899/hnnnews/hnnnews/index.m3u8 | https://ott.livelegitpro.in:9899/hnnnews/hnnnews/index.m3u8 |
| Working | Same | IBC 24 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/0bfbd0b9de7f4407949202296560c0fe/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/0bfbd0b9de7f4407949202296560c0fe/index.m3u8 |
| Working | Same | Ind 24 | https://livestream.jswk.online/ind24/live/index.m3u8 | https://livestream.jswk.online/ind24/live/index.m3u8 |
| Working | Same | India Daily Live | https://indiadaily.ottlive.co.in/indiadailylive/index.m3u8 | https://indiadaily.ottlive.co.in/indiadailylive/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",India News | https://fta.ektv.in/live/297/master.m3u8 | https://fta.ektv.in/live/297/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",India News Haryana | https://fta.ektv.in/live/590/master.m3u8 | https://fta.ektv.in/live/590/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",India News Madhya Pradesh/Chhattisgarh | https://fta.ektv.in/live/600/master.m3u8 | https://fta.ektv.in/live/600/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",India News Rajasthan | https://fta.ektv.in/live/601/master.m3u8 | https://fta.ektv.in/live/601/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",India News Uttar Pradesh | https://fta.ektv.in/live/304/master.m3u8 | https://fta.ektv.in/live/304/master.m3u8 |
| Working | Same | India TV | https://vg-indiatv-waves.vgcdn.net/vglive-sk-394591/playlist.m3u8 | https://vg-indiatv-waves.vgcdn.net/vglive-sk-394591/playlist.m3u8 |
| Working | Same | India TV Speed News | https://cc-lyf4c0hwzg5dd.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-lyf4c0hwzg5dd/v1/vglive-sk-479089/main.m3u8 | https://cc-lyf4c0hwzg5dd.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-lyf4c0hwzg5dd/v1/vglive-sk-479089/main.m3u8 |
| Working | Same | India Voice | https://d1msejlow1t3l4.cloudfront.net/fta/indiavoice/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/indiavoice/playlist.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",INH 24x7 | https://fta.ektv.in/live/99/99_0.m3u8 | https://fta.ektv.in/live/99/99_0.m3u8 |
| Working | Same | Janta TV | https://live.jswk.online/IK_RTPM/live/index.m3u8 | https://live.jswk.online/IK_RTPM/live/index.m3u8 |
| Working | Same | Jantantra TV | https://d1msejlow1t3l4.cloudfront.net/fta/jantantratv/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/jantantratv/playlist.m3u8 |
| Working | Same | JK 24x7 News | https://samitaorigin.tangotv.in/JKL24X7NEWS/SAMITAORIGIN/index.m3u8 | https://samitaorigin.tangotv.in/JKL24X7NEWS/SAMITAORIGIN/index.m3u8 |
| Non-working | Same | K News India | https://legitpro.co.in/knews/index.m3u8 | https://legitpro.co.in/knews/index.m3u8 |
| Working | Same | Kadak | https://n18syndication.akamaized.net/bpk-tv/Kadak_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/Kadak_NW18_MOB/output01/master.m3u8 |
| Working | Same | Kashish News | https://server.thelegitpro.in/kashishnews/kashishnews/index.m3u8 | https://server.thelegitpro.in/kashishnews/kashishnews/index.m3u8 |
| Working | Same | KBC News | https://stream.ottlive.co.in/kbcnews/index.m3u8 | https://stream.ottlive.co.in/kbcnews/index.m3u8 |
| Working | Same | KBP Times | https://kbpnews.cloud/Kbptimes/Kbptimeslive/video.m3u8 | https://kbpnews.cloud/Kbptimes/Kbptimeslive/video.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",Khabar Fast | https://fta.ektv.in/live/740/master.m3u8 | https://fta.ektv.in/live/740/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",Khabrain Abhi Tak | https://fta.ektv.in/live/308/master.m3u8 | https://fta.ektv.in/live/308/master.m3u8 |
| Working | Same | Live Times | https://stream.ottlive.co.in/livetimetv/index.m3u8 | https://stream.ottlive.co.in/livetimetv/index.m3u8 |
| Working | Same | Media9 | https://media9news.akamaized.net/media9/hls/media9tv.m3u8 | https://media9news.akamaized.net/media9/hls/media9tv.m3u8 |
| Non-working | Same | Nagaland TV | https://mumt06.tangotv.in/qYyB8fXVNAGALANDTV/index.m3u8 | https://mumt06.tangotv.in/qYyB8fXVNAGALANDTV/index.m3u8 |
| Working | Same | Nation News | https://server.playontv.in/nationnews/index.m3u8 | https://server.playontv.in/nationnews/index.m3u8 |
| Working | Same | Naxatra News Hindi | https://d2gvyg6lvauoko.cloudfront.net/230226/naxatranewshindi/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://d2gvyg6lvauoko.cloudfront.net/230226/naxatranewshindi/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | NDTV Good Times | https://amg01448-samsungin-ndtvgoodtimes-samsungin-ad-gp.amagi.tv/playlist/amg01448-samsungin-ndtvgoodtimes-samsungin/playlist.m3u8 | https://amg01448-samsungin-ndtvgoodtimes-samsungin-ad-gp.amagi.tv/playlist/amg01448-samsungin-ndtvgoodtimes-samsungin/playlist.m3u8 |
| Working | Same | NDTV India | https://backupndtvindiaelemarchana.akamaized.net/hls/live/2004134/ndtvindia/master_1.m3u8 | https://backupndtvindiaelemarchana.akamaized.net/hls/live/2004134/ndtvindia/master_1.m3u8 |
| Working | Same | NDTV Madhya Pradesh Chhattisgarh | https://ndtvregional.akamaized.net/hls/live/2102726-b/ndtvmpcg/master_1.m3u8 | https://ndtvregional.akamaized.net/hls/live/2102726-b/ndtvmpcg/master_1.m3u8 |
| Working | Same | NDTV Rajasthan | https://ndtvregional.akamaized.net/hls/live/2102726-b/ndtvraj/master_1.m3u8 | https://ndtvregional.akamaized.net/hls/live/2102726-b/ndtvraj/master_1.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",NE News | https://fta.ektv.in/live/681/master.m3u8 | https://fta.ektv.in/live/681/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",News 1 India | https://fta.ektv.in/live/102/102_0.m3u8 | https://fta.ektv.in/live/102/102_0.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="General",News 11 | https://fta.ektv.in/live/307/master.m3u8 | https://fta.ektv.in/live/307/master.m3u8 |
| Working | Same | News18 Bihar Jharkhand | https://n18syndication.akamaized.net/bpk-tv/News18_Bihar_Jharkhand_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_Bihar_Jharkhand_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Delhi NCR JK | https://n18syndication.akamaized.net/bpk-tv/News18_JKLH_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_JKLH_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 India | https://n18syndication.akamaized.net/bpk-tv/News18_India_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_India_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Madhya Pradesh/Chhattisgarh | https://n18syndication.akamaized.net/bpk-tv/News18_MP_Chhattisgarh_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_MP_Chhattisgarh_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Punjab/Haryana/Himachal | https://n18syndication.akamaized.net/bpk-tv/News18_Punjab_Haryana_HP_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_Punjab_Haryana_HP_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Rajasthan | https://n18syndication.akamaized.net/bpk-tv/News18_Rajasthan_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_Rajasthan_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Uttar Pradesh Uttarakhand | https://n18syndication.akamaized.net/bpk-tv/News18_UP_Uttarakhand_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_UP_Uttarakhand_NW18_MOB/output01/master.m3u8 |
| Non-working | Same | News 24 (India) | https://vidcdn.vidgyor.com/news24-origin/liveabr/playlist.m3u8 | https://vidcdn.vidgyor.com/news24-origin/liveabr/playlist.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",News 24 MP & Chhattisgarh | https://fta.ektv.in/live/303/master.m3u8 | https://fta.ektv.in/live/303/master.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",News Daily 24 | https://fta.ektv.in/live/316/master.m3u8 | https://fta.ektv.in/live/316/master.m3u8 |
| Working | Same | News Hour | https://mumt07.tangotv.in/zHjX9OFlNEWSHOUR/index.m3u8 | https://mumt07.tangotv.in/zHjX9OFlNEWSHOUR/index.m3u8 |
| Working | Same | News India 24x7 | https://stream.ottlive.co.in/newsindia/index.m3u8 | https://stream.ottlive.co.in/newsindia/index.m3u8 |
| Working | Same | News Leader | https://stream.ottlive.co.in/newsleader/index.m3u8 | https://stream.ottlive.co.in/newsleader/index.m3u8 |
| Working | Same | News Nation 81 | https://live.newsnation81.com/newsnation81/newsnation81/index.m3u8 | https://live.newsnation81.com/newsnation81/newsnation81/index.m3u8 |
| Working | Same | News Nation | https://cc-52950m0v2qv0p.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-52950m0v2qv0p/nntv/national/index.m3u8 | https://cc-52950m0v2qv0p.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-52950m0v2qv0p/nntv/national/index.m3u8 |
| Working | Same | News State MP & CHG | https://jmp2.uk/stvp-IN4000012ML | https://jmp2.uk/stvp-IN4000012ML |
| Working | Same | News State Punjab Haryana Himachal | https://jmp2.uk/stvp-IN300083R1 | https://jmp2.uk/stvp-IN300083R1 |
| Working | Same | News State UP & UK | https://jmp2.uk/stvp-IN3000846P | https://jmp2.uk/stvp-IN3000846P |
| Working | Same | News TV India | https://streamlive.livebox.co.in/NewsTVIndiahls/live.m3u8 | https://streamlive.livebox.co.in/NewsTVIndiahls/live.m3u8 |
| Working | Same | Non Stop Bharat | https://mumt07.tangotv.in/zHjX9OFlCHAUKASTV/index.m3u8 | https://mumt07.tangotv.in/zHjX9OFlCHAUKASTV/index.m3u8 |
| Working | Same | like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0" group-title="News",Northeast Live | https://server.thelegitpro.in/northeastlive/northeastlive/index.fmp4.m3u8 | https://server.thelegitpro.in/northeastlive/northeastlive/index.fmp4.m3u8 |
| Working | Same | NSC9 News | https://legitpro.co.in/nsc9/index.m3u8 | https://legitpro.co.in/nsc9/index.m3u8 |
| Working | Same | Only Bharat | https://mumt07.tangotv.in/zHjX9OFlONLYBHARAT/index.m3u8 | https://mumt07.tangotv.in/zHjX9OFlONLYBHARAT/index.m3u8 |
| Non-working | Same | Pratham News | https://mumt03.tangotv.in/Dsly5z3HPRATHAMNEWS/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HPRATHAMNEWS/index.m3u8 |
| Working | Same | Prime News | https://stream.ottlive.co.in/primenews/index.m3u8 | https://stream.ottlive.co.in/primenews/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",Public First | https://fta.ektv.in/live/237/master.m3u8 | https://fta.ektv.in/live/237/master.m3u8 |
| Non-working | Same | Raj Pariwar | https://livestream.rajtvnet.in/hlslive/Admin/px08241089/live/Raj_Pariwar/master_1.m3u8 | https://livestream.rajtvnet.in/hlslive/Admin/px08241089/live/Raj_Pariwar/master_1.m3u8 |
| Working | Same | Republic Bharat | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/RepublicBharat.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/RepublicBharat.m3u8 |
| Working | Same | Sach Bedhadak | https://sbnews.nexcdn.online/sbnews/live/index.m3u8 | https://sbnews.nexcdn.online/sbnews/live/index.m3u8 |
| Working | Same | Sadhna News Madhya Pradesh/Chhattisgarh | https://mumt04.tangotv.in/m18aqlK4SADHNEWSPMRAJ/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4SADHNEWSPMRAJ/index.m3u8 |
| Working | Same | Sadhna Plus News | https://6n3yow8pl9ok-hls-live.5centscdn.com/sadhananewstv/live.stream/playlist.m3u8 | https://6n3yow8pl9ok-hls-live.5centscdn.com/sadhananewstv/live.stream/playlist.m3u8 |
| Non-working | Same | Sahana News | https://mumt03.tangotv.in/Dsly5z3HSAHANANEWS/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HSAHANANEWS/index.m3u8 |
| Working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",Samachar Plus 24x7 | https://fta.ektv.in/live/589/master.m3u8 | https://fta.ektv.in/live/589/master.m3u8 |
| Non-working | Same | Star Bharat (India) HD | http://103.135.253.32:8080/STAR-BHARAT/index.m3u8 | http://103.135.253.32:8080/STAR-BHARAT/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",STV Haryana News | https://fta.ektv.in/live/607/master.m3u8 | https://fta.ektv.in/live/607/master.m3u8 |
| Working | Same | Sudarshan News | https://ott.livelegitpro.in/sudarshannews/sudarshannews/tracks-v1/index.fmp4.m3u8 | https://ott.livelegitpro.in/sudarshannews/sudarshannews/tracks-v1/index.fmp4.m3u8 |
| Working | Same | Surya Samachar | https://d1msejlow1t3l4.cloudfront.net/fta/suryasamachar/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/suryasamachar/playlist.m3u8 |
| Working | Same | Swadesh News | https://cdn.pishow.tv/ott/live/465/master.m3u8 | https://cdn.pishow.tv/ott/live/465/master.m3u8 |
| Working | Same | Swaraj Express SMBC | https://d1msejlow1t3l4.cloudfront.net/fta/swarajexpresssmbc/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/swarajexpresssmbc/playlist.m3u8 |
| Working | Same | The Voice TV | https://legitpro.co.in/thevoicetv/thevoicetv/index.m3u8 | https://legitpro.co.in/thevoicetv/thevoicetv/index.m3u8 |
| Non-working | Same | Times Now (720p) | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/timesnow/timesnow_master.m3u8 | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/timesnow/timesnow_master.m3u8 |
| Working | Same | Times Now Navbharat | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/a5ee7c4e7a2a4b15a22a3bcf523b9776/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/a5ee7c4e7a2a4b15a22a3bcf523b9776/index.m3u8 |
| Working | Same | Times Now Navbharat HD | https://yupprestreamliveus.akamaized.net/v1/vglive-sk-717514/main.m3u8 | https://yupprestreamliveus.akamaized.net/v1/vglive-sk-717514/main.m3u8 |
| Working | Same | TNP News | https://server.thelegitpro.in/tnpnews/tnpnews/index.m3u8 | https://server.thelegitpro.in/tnpnews/tnpnews/index.m3u8 |
| Working | Same | TTN24 | https://stream.joytvindia.com/stream/hls/ttn24/index.m3u8 | https://stream.joytvindia.com/stream/hls/ttn24/index.m3u8 |
| Working | Same | TV7 Bharat | https://vglivessai.akamaized.net/sg/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/797fcff8-10d6-4c9c-a409-8d0c4fa5c8dd/index.m3u8 | https://vglivessai.akamaized.net/sg/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/797fcff8-10d6-4c9c-a409-8d0c4fa5c8dd/index.m3u8 |
| Working | Same | TV7 National | https://stream.ottlive.co.in/tv7national/index.m3u8 | https://stream.ottlive.co.in/tv7national/index.m3u8 |
| Working | Same | TV9 Bharatvarsh | https://amg01106-amg01106c2-amgplt0747.playout.now3.amagi.tv/amg01106c2/hls.m3u8 | https://amg01106-amg01106c2-amgplt0747.playout.now3.amagi.tv/amg01106c2/hls.m3u8 |
| Working | Same | TV27 News | https://stream.ottlive.co.in/tv27/index.m3u8 | https://stream.ottlive.co.in/tv27/index.m3u8 |
| Working | Same | TV30 India | https://stream.tv30bharat.com/hls/shree/bhattji.m3u8 | https://stream.tv30bharat.com/hls/shree/bhattji.m3u8 |
| Working | Same | TV45 | https://server.livelegitpro.in/bnews24/bnews24/video.m3u8 | https://server.livelegitpro.in/bnews24/bnews24/video.m3u8 |
| Working | Same | UP NOW | http://45.122.122.61:8080/UPNOW/video.m3u8 | http://45.122.122.61:8080/UPNOW/video.m3u8 |
| Non-working | Same | VIP News | https://live.vipnews24x7.co.in/vipnews24x7/d0dbe915091d400bd8ee7f27f0791303.sdp/playlist.m3u8 | https://live.vipnews24x7.co.in/vipnews24x7/d0dbe915091d400bd8ee7f27f0791303.sdp/playlist.m3u8 |
| Working | Same | Vistaar News | https://stream.ottlive.co.in/vistaartv/index.m3u8 | https://stream.ottlive.co.in/vistaartv/index.m3u8 |
| Working | Same | Zee Bharat | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeehindustan/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/96bbab12-582e-4540-af70-510ab6824581/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeehindustan/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/96bbab12-582e-4540-af70-510ab6824581/main.m3u8 |
| Working | Same | Zee Delhi NCR Haryana | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeedelhincr/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/cc483a15-1b39-4642-872d-5d08d362ed01/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeedelhincr/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/cc483a15-1b39-4642-872d-5d08d362ed01/main.m3u8 |
| Working | Same | Zee Madhya Pradesh Chhattisgarh | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeemadhyachhattisgarh/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/2ab17056-6187-4f0e-a34d-f436ac479d6c/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeemadhyachhattisgarh/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/2ab17056-6187-4f0e-a34d-f436ac479d6c/main.m3u8 |
| Working | Same | Zee News | https://dknttpxmr0dwf.cloudfront.net/index_57.m3u8 | https://dknttpxmr0dwf.cloudfront.net/index_57.m3u8 |
| Working | Same | Zee Rajasthan | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeerajashthannews/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/8e864b9a-1681-41a0-99a6-387490bc5b24/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeerajashthannews/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/8e864b9a-1681-41a0-99a6-387490bc5b24/main.m3u8 |
| Working | Same | Zee Uttar Pradesh/Uttarakhand | https://duw35ict5q7th.cloudfront.net/index_3.m3u8 | https://duw35ict5q7th.cloudfront.net/index_3.m3u8 |
| Working | Same | Mahua Khabar | https://cdn.ottlive.co.in/mahuakhabar/index.m3u8 | https://cdn.ottlive.co.in/mahuakhabar/index.m3u8 |
| Working | Same | Zee Bihar Jharkhand | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/ZeeBiharJharkhand.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/ZeeBiharJharkhand.m3u8 |
| Working | Same | HMTV (India) | https://cdn.pishow.tv/ott/live/280/master.m3u8 | https://cdn.pishow.tv/ott/live/280/master.m3u8 |
| Working | Same | India Today | https://d2lk5u59tns74c.cloudfront.net/out/v1/d4435039c7d1433d9b9d0b6cdc9dd4ff/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/d4435039c7d1433d9b9d0b6cdc9dd4ff/index.m3u8 |
| Working | Same | Mirror Now | https://dai.google.com/linear/hls/event/ClPOullTQky5vGPf7fMZ8g/master.m3u8 | https://dai.google.com/linear/hls/event/ClPOullTQky5vGPf7fMZ8g/master.m3u8 |
| Working | Same | NDTV 24x7 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/NDTV24x7.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/NDTV24x7.m3u8 |
| Working | Same | NDTV | https://yupprestreamliveus.akamaized.net/v1/vglive-sk-401405/0194a671d8dd1ebd416a3e0a8a4524/0194a67abb941ebd47043cd206ba4f/main.m3u8 | https://yupprestreamliveus.akamaized.net/v1/vglive-sk-401405/0194a671d8dd1ebd416a3e0a8a4524/0194a67abb941ebd47043cd206ba4f/main.m3u8 |
| Working | Same | NDTV Profit | https://ndtvprofit.akamaized.net/hls/live/2107404/ndtvprofit/chunklist_5.m3u8 | https://ndtvprofit.akamaized.net/hls/live/2107404/ndtvprofit/chunklist_5.m3u8 |
| Non-working | Same | NewsX | https://mumbai-edge.smartplaytv.in/NewsX/index.m3u8 | https://mumbai-edge.smartplaytv.in/NewsX/index.m3u8 |
| Working | Same | NewsX World | https://cdn.pishow.tv/ott/live/1049/master.m3u8 | https://cdn.pishow.tv/ott/live/1049/master.m3u8 |
| Working | Same | Republic TV | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/RepublicTV.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/RepublicTV.m3u8 |

## Science

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | Astroscience | https://yuppnimrestreammum.akamaized.net/181224/smil:astrotech.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yuppnimrestreammum.akamaized.net/181224/smil:astrotech.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Non-working | Same | Discovery Channel (India) HD | http://103.135.253.32:8080/DISCOVERY/index.m3u8 | http://103.135.253.32:8080/DISCOVERY/index.m3u8 |
| Working | Same | History TV18 HD (1080p) | https://amg01448-amg01448c16-samsung-in-3495.playouts.now.amagi.tv/playlist/amg01448-samsungindia-historychannelenglish-samsungin/playlist.m3u8 | https://amg01448-amg01448c16-samsung-in-3495.playouts.now.amagi.tv/playlist/amg01448-samsungindia-historychannelenglish-samsungin/playlist.m3u8 |

## Sports

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | DD Sports | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/b17adfe543354fdd8d189b110617cddd/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/b17adfe543354fdd8d189b110617cddd/index.m3u8 |
| Working | Same | DD Sports HD | https://cdn.pishow.tv/ott/live/1161/master.m3u8 | https://cdn.pishow.tv/ott/live/1161/master.m3u8 |
| Working | Same | Kabaddi 24x7 | https://samitaorigin.tangotv.in/KABADDI24X7/SAMITAORIGIN/index.m3u8 | https://samitaorigin.tangotv.in/KABADDI24X7/SAMITAORIGIN/index.m3u8 |
| Non-working | Same | T Sports | https://tvsen5.aynaott.com/TnMn5kZz8aLm/index.m3u8 | https://tvsen5.aynaott.com/TnMn5kZz8aLm/index.m3u8 |
| Working | Same | Cricket Gold | https://streams2.sofast.tv/ptnr-yupptv/title-cricketgold/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/b2048bb8-1686-4432-aa50-647245383e0c/manifest.m3u8 | https://streams2.sofast.tv/ptnr-yupptv/title-cricketgold/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/b2048bb8-1686-4432-aa50-647245383e0c/manifest.m3u8 |
| Working | Same | Fast Sports | http://s7.merlive.am/Fastsports/index.m3u8 | http://s7.merlive.am/Fastsports/index.m3u8 |
| Working | Same | Fox Sports 1 | http://85.237.89.160:9590/usa-s/FOX-SPORTS-1/index.m3u8 | http://85.237.89.160:9590/usa-s/FOX-SPORTS-1/index.m3u8 |
| Non-working | Same | Fox Sports 2 | https://tvsen7.aynascope.net/foxsports2/index.m3u8 | https://tvsen7.aynascope.net/foxsports2/index.m3u8 |
| Working | Same | Fox Sports | http://138.59.227.20:8000/play/a085/index.m3u8 | http://138.59.227.20:8000/play/a085/index.m3u8 |
| Working | Same | Fox Sports HD | http://45.184.109.10/live/69393EAE6ADBC65A68F942022362A202/1552.m3u8 | http://45.184.109.10/live/69393EAE6ADBC65A68F942022362A202/1552.m3u8 |
| Working | Same | Fox Sports News | https://skynewsau-live-premium.akamaized.net/hls/live/2105307/foxsportsnews/live_1080p.m3u8 | https://skynewsau-live-premium.akamaized.net/hls/live/2105307/foxsportsnews/live_1080p.m3u8 |
| Non-working | Same | PTV Sports | http://103.250.28.74:8000/play/a019/index.m3u8 | http://103.250.28.74:8000/play/a019/index.m3u8 |
| Working | Same | T Sports 7 | https://live-us1.thaimomo.com/live-as/chtsport-1/playlist.m3u8 | https://live-us1.thaimomo.com/live-as/chtsport-1/playlist.m3u8 |
| Non-working | Same | TNT Sports 1 | http://37.49.224.5/stream/1/index.m3u8 | http://37.49.224.5/stream/1/index.m3u8 |
| Non-working | Same | TNT Sports 2 | http://37.49.224.5/stream/2/index.m3u8 | http://37.49.224.5/stream/2/index.m3u8 |
| Non-working | Same | TNT Sports 3 | http://37.49.224.5/stream/3/index.m3u8 | http://37.49.224.5/stream/3/index.m3u8 |
| Non-working | Same | TNT Sports 4 | http://37.49.224.5/stream/4/index.m3u8 | http://37.49.224.5/stream/4/index.m3u8 |
| Working | Same | TNT Sports (Argentina) | http://45.184.109.10/live/69393EAE6ADBC65A68F942022362A202/86.m3u8 | http://45.184.109.10/live/69393EAE6ADBC65A68F942022362A202/86.m3u8 |
| Working | Same | TNT Sports (Argentina) SD | http://181.78.79.131:8000/play/a0mo | http://181.78.79.131:8000/play/a0mo |
| Working | Same | TNT Sports (Chile) | http://209.45.101.130:8040/play/a03s/index.m3u8 | http://209.45.101.130:8040/play/a03s/index.m3u8 |
| Working | Same | TNT Sports Premium ArgentinaHD | http://181.78.79.131:8000/play/a0q9 | http://181.78.79.131:8000/play/a0q9 |
| Working | Same | TNT Sports Premium HD | https://play-fulltv.com.ar/playtvpre/tntsportschile.m3u8 | https://play-fulltv.com.ar/playtvpre/tntsportschile.m3u8 |
| Non-working | Same | Willow | http://tvsen5.aynascope.net/willowhd/index.m3u8 | http://tvsen5.aynascope.net/willowhd/index.m3u8 |
| Working | Same | Willow Sports | https://d36r8jifhgsk5j.cloudfront.net/Willow_TV.m3u8 | https://d36r8jifhgsk5j.cloudfront.net/Willow_TV.m3u8 |


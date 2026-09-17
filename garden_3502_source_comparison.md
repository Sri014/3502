# Garden vs 3502 — Actual Source Comparison

- Garden actual source entries after Garden filters: **425**
- 3502 actual source: **https://iptv-org.github.io/iptv/index.m3u**
- Matching rule: **exact stream URL**
- Different/Not Found rule: channel name is used only after exact URL is absent.

- Same: **425**
- Different URL: **0**
- Not Found: **0**

## Business

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | CNBC Awaaz | https://n18syndication.akamaized.net/bpk-tv/CNBC_Awaaz_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/CNBC_Awaaz_NW18_MOB/output01/master.m3u8 |
| Working | Same | Zee Business | https://dwby15d04agvq.cloudfront.net/index_5.m3u8 | https://dwby15d04agvq.cloudfront.net/index_5.m3u8 |
| Working | Same | CNBC Bajar | https://n18syndication.akamaized.net/bpk-tv/CNBC_Bazaar_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/CNBC_Bazaar_NW18_MOB/output01/master.m3u8 |
| Working | Same | CNBC TV18 | https://n18syndication.akamaized.net/bpk-tv/CNBC_TV18_NW18_MOB/output01/index.m3u8 | https://n18syndication.akamaized.net/bpk-tv/CNBC_TV18_NW18_MOB/output01/index.m3u8 |
| Working | Same | CNBC TV18 Prime HD | https://n18syndication.akamaized.net/bpk-tv/CNBC_Tv18_Prime_HD_NW18_MOB/output01/index.m3u8 | https://n18syndication.akamaized.net/bpk-tv/CNBC_Tv18_Prime_HD_NW18_MOB/output01/index.m3u8 |
| Non-working | Same | ET Now (720p) | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/etnow/etnow_master.m3u8 | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/etnow/etnow_master.m3u8 |

## Cartoon

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | Disney Channel | http://202.70.146.135:8000/play/a01q/index.m3u8 | http://202.70.146.135:8000/play/a01q/index.m3u8 |
| Non-working | Same | Disney Channel HD | http://66.102.126.10:8000/play/a013/index.m3u8 | http://66.102.126.10:8000/play/a013/index.m3u8 |
| Working | Same | Epic Kids Digital | https://cc-t8lqe1o99pszu.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-t8lqe1o99pszu/playlist.m3u8 | https://cc-t8lqe1o99pszu.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-t8lqe1o99pszu/playlist.m3u8 |
| Working | Same | ETV Bal Bharat | http://103.185.24.134:3001/ETV-BAL-BHARAT/index.m3u8 | http://103.185.24.134:3001/ETV-BAL-BHARAT/index.m3u8 |
| Working | Same | Hungama TV | http://103.185.24.134:3001/HUNGAMA/index.m3u8 | http://103.185.24.134:3001/HUNGAMA/index.m3u8 |
| Working | Same | Nick Jr. | http://103.185.24.134:3001/NICK-JR/index.m3u8 | http://103.185.24.134:3001/NICK-JR/index.m3u8 |
| Working | Same | Nickelodeon | http://103.185.24.134:3001/NICK/index.m3u8 | http://103.185.24.134:3001/NICK/index.m3u8 |
| Working | Same | Sonic | http://103.185.24.134:3001/SONIC/index.m3u8 | http://103.185.24.134:3001/SONIC/index.m3u8 |
| Working | Same | Sony Yay! | https://cloudplay-sonyliv.pages.dev/yay.m3u8 | https://cloudplay-sonyliv.pages.dev/yay.m3u8 |
| Working | Same | Super Hungama | http://103.185.24.134:3001/SUPER-HUNGAMA/index.m3u8 | http://103.185.24.134:3001/SUPER-HUNGAMA/index.m3u8 |
| Working | Same | The Jungle Book | https://cc-4bhi5osabejc9.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-4bhi5osabejc9/junglebook.m3u8 | https://cc-4bhi5osabejc9.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-4bhi5osabejc9/junglebook.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment;Kids",Unique TV | http://103.175.73.12:8080/live/688/master.m3u8 | http://103.175.73.12:8080/live/688/master.m3u8 |
| Working | Same | WOW Kidz | https://yuppparoriglin.akamaized.net/181224/smil:wowkidzhindi.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yuppparoriglin.akamaized.net/181224/smil:wowkidzhindi.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | Disney International HD | http://202.70.146.135:8000/play/a04p/index.m3u8 | http://202.70.146.135:8000/play/a04p/index.m3u8 |
| Non-working | Same | Nick HD+ | http://103.72.101.252:8080/live/1226.m3u8 | http://103.72.101.252:8080/live/1226.m3u8 |
| Working | Same | WOW Kidz | https://yuppparoriglin.akamaized.net/181224/smil:wowkidztelgu.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yuppparoriglin.akamaized.net/181224/smil:wowkidztelgu.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Non-working | Same | ZB Cartoon | https://server.zillarbarta.com/zbcatun/video.m3u8 | https://server.zillarbarta.com/zbcatun/video.m3u8 |

## Devotional

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | Aadinath TV | https://mumt01.tangotv.in/O5aw8Zn3AADINATHTV/index.m3u8 | https://mumt01.tangotv.in/O5aw8Zn3AADINATHTV/index.m3u8 |
| Working | Same | Aastha | https://aasthaott.akamaized.net/110923/smil:aasthatv.smil/index.m3u8 | https://aasthaott.akamaized.net/110923/smil:aasthatv.smil/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Religious",Aastha Bhajan | http://103.175.73.12:8080/live/339/master.m3u8 | http://103.175.73.12:8080/live/339/master.m3u8 |
| Working | Same | Aastha Prime 1 | https://aasthaott.akamaized.net/110923/smil:aasthaprime1.smil/master.m3u8 | https://aasthaott.akamaized.net/110923/smil:aasthaprime1.smil/master.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Religious",Aastha SD | http://103.175.73.12:8080/live/338/master.m3u8 | http://103.175.73.12:8080/live/338/master.m3u8 |
| Working | Same | ABN TV India | https://mediaserver.abnvideos.com/streams/abntvindia.m3u8 | https://mediaserver.abnvideos.com/streams/abntvindia.m3u8 |
| Working | Same | Adhyatm TV | https://mumbai-edge.smartplaytv.in/AdhyatmTV/index.m3u8 | https://mumbai-edge.smartplaytv.in/AdhyatmTV/index.m3u8 |
| Working | Same | Anand TV | https://live.legitpro.co.in/anandtv/index.m3u8 | https://live.legitpro.co.in/anandtv/index.m3u8 |
| Working | Same | Anand Wari TV | https://mumt03.tangotv.in/Dsly5z3HANANDWARITV/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HANANDWARITV/index.m3u8 |
| Non-working | Same | Aradana TV | https://mumbai-edge.smartplaytv.in/AradanaTV/index.m3u8 | https://mumbai-edge.smartplaytv.in/AradanaTV/index.m3u8 |
| Working | Same | Awakening TV | https://mumt03.tangotv.in/Dsly5z3HAWAKENINGTV/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HAWAKENINGTV/index.m3u8 |
| Working | Same | Bhakti Sagar | https://mumt05.tangotv.in/87NeALx2BHAKTISAGAR/index.m3u8 | https://mumt05.tangotv.in/87NeALx2BHAKTISAGAR/index.m3u8 |
| Working | Same | Channel Divya | https://vg-pitaaratvlive.akamaized.net/v1/vglive-sk-906482/playlist.m3u8 | https://vg-pitaaratvlive.akamaized.net/v1/vglive-sk-906482/playlist.m3u8 |
| Working | Same | Darshan 24 | https://mumt05.tangotv.in/87NeALx2DARSHAN24/index.m3u8 | https://mumt05.tangotv.in/87NeALx2DARSHAN24/index.m3u8 |
| Working | Same | Dheeran TV | https://live.we2live.in/dheerantv/dheerantv/playlist.m3u8 | https://live.we2live.in/dheerantv/dheerantv/playlist.m3u8 |
| Non-working | Same | Fateh TV | http://180.188.254.253/live/FATEHTVHD.m3u8 | http://180.188.254.253/live/FATEHTVHD.m3u8 |
| Non-working | Same | God Stands TV Hindi | https://online.godstands.tv:5443/WebRTCApp/streams/HindiStreaming.m3u8 | https://online.godstands.tv:5443/WebRTCApp/streams/HindiStreaming.m3u8 |
| Working | Same | GurSikh Sabha TV (720p) | http://cdn12.henico.net:8080/live/gsctv/index.m3u8 | http://cdn12.henico.net:8080/live/gsctv/index.m3u8 |
| Working | Same | Hare Krsna TV | https://hktv.harekrsnatv.com/HKTV/HKWebApp/manifest.mpd | https://hktv.harekrsnatv.com/HKTV/HKWebApp/manifest.mpd |
| Non-working | Same | Hosanna TV Hindi | https://mumbai-edge.smartplaytv.in/HosannaTV/index.m3u8 | https://mumbai-edge.smartplaytv.in/HosannaTV/index.m3u8 |
| Working | Same | Ishwar Bhakti TV | https://6n3yow8pl9ok-hls-live.5centscdn.com/ishwartvlive/tv.stream/playlist.m3u8 | https://6n3yow8pl9ok-hls-live.5centscdn.com/ishwartvlive/tv.stream/playlist.m3u8 |
| Working | Same | Jinvani Channel | https://cdn.pishow.tv/ott/live/989/master.m3u8 | https://cdn.pishow.tv/ott/live/989/master.m3u8 |
| Non-working | Same | Kanshi TV (720p) | https://live.kanshitv.co.uk/mobile/kanshitvkey.m3u8 | https://live.kanshitv.co.uk/mobile/kanshitvkey.m3u8 |
| Working | Same | Lighting Lives Blessing Nations TV South Asia (LLBN) | https://brightstar-southasia-pull-secure.akamaized.net/brightstarsouthasia/stream.m3u8 | https://brightstar-southasia-pull-secure.akamaized.net/brightstarsouthasia/stream.m3u8 |
| Working | Same | Mercy TV | https://5dd3981940faa.streamlock.net/mercytv/mercytv/playlist.m3u8 | https://5dd3981940faa.streamlock.net/mercytv/mercytv/playlist.m3u8 |
| Working | Same | MH One Shraddha | https://mumt01.tangotv.in/O5aw8Zn3MHONESHRADDHA/index.m3u8 | https://mumt01.tangotv.in/O5aw8Zn3MHONESHRADDHA/index.m3u8 |
| Working | Same | MTA2 Europe | https://chlivemta1.akamaized.net/hls/live/2008145/mta2/playlist.m3u8 | https://chlivemta1.akamaized.net/hls/live/2008145/mta2/playlist.m3u8 |
| Working | Same | MTA7 Asia | https://livemtaasia.akamaized.net/hls/live/2039224/mtaasia2/playlist.m3u8 | https://livemtaasia.akamaized.net/hls/live/2039224/mtaasia2/playlist.m3u8 |
| Working | Same | Namdhari (404p) | https://namdhari.tv/live/sbs1.m3u8 | https://namdhari.tv/live/sbs1.m3u8 |
| Working | Same | Paras Gold | https://mumt04.tangotv.in/m18aqlK4PARASGOLD/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4PARASGOLD/index.m3u8 |
| Working | Same | Peace of Mind TV | https://yuppnimrestreammum.akamaized.net/181224/smil:peaceofmind.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yuppnimrestreammum.akamaized.net/181224/smil:peaceofmind.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | Sadhna | https://6n3yow8pl9ok-hls-live.5centscdn.com/sadhanalivetv/live.stream/playlist.m3u8 | https://6n3yow8pl9ok-hls-live.5centscdn.com/sadhanalivetv/live.stream/playlist.m3u8 |
| Working | Same | Sadhna TV | https://mumt05.tangotv.in/87NeALx2SADHNATV/index.m3u8 | https://mumt05.tangotv.in/87NeALx2SADHNATV/index.m3u8 |
| Working | Same | Sanskar TV | https://d26idhjf0y1p2g.cloudfront.net/out/v1/cd66dd25b9774cb29943bab54bbf3e2f/index.m3u8 | https://d26idhjf0y1p2g.cloudfront.net/out/v1/cd66dd25b9774cb29943bab54bbf3e2f/index.m3u8 |
| Working | Same | Sanskar UK | https://d34z4embz0hjf6.cloudfront.net/out/v1/7ac2789ff9a544a49337d1ffc54ce61c/index.m3u8 | https://d34z4embz0hjf6.cloudfront.net/out/v1/7ac2789ff9a544a49337d1ffc54ce61c/index.m3u8 |
| Working | Same | Sanskar USA | https://d2netiedy8cz3x.cloudfront.net/out/v1/9bf6fa4ac8d6432cb98da13b121ba3c2/index.m3u8 | https://d2netiedy8cz3x.cloudfront.net/out/v1/9bf6fa4ac8d6432cb98da13b121ba3c2/index.m3u8 |
| Working | Same | Sanskar Web TV | https://deatfcv3xdvi3.cloudfront.net/out/v1/7a43dd2f64e34ec28da1b4bd6923251a/index.m3u8 | https://deatfcv3xdvi3.cloudfront.net/out/v1/7a43dd2f64e34ec28da1b4bd6923251a/index.m3u8 |
| Working | Same | Sarv Dharm Sangam | https://mumt01.tangotv.in/O5aw8Zn3SARAVDHARAMSANGAM/index.m3u8 | https://mumt01.tangotv.in/O5aw8Zn3SARAVDHARAMSANGAM/index.m3u8 |
| Working | Same | Satsang TV | https://d2vfwvjxwtwq1t.cloudfront.net/out/v1/6b24239d5517495b986e7705490c6e65/index.m3u8 | https://d2vfwvjxwtwq1t.cloudfront.net/out/v1/6b24239d5517495b986e7705490c6e65/index.m3u8 |
| Working | Same | Satsang Web TV | https://d1ji7e9jbzm5g8.cloudfront.net/out/v1/769f22f64d80442889306b9c4abea63c/index.m3u8 | https://d1ji7e9jbzm5g8.cloudfront.net/out/v1/769f22f64d80442889306b9c4abea63c/index.m3u8 |
| Working | Same | Shubhsandesh TV | https://mumt03.tangotv.in/Dsly5z3HSHUBHSANDESH/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HSHUBHSANDESH/index.m3u8 |
| Working | Same | Soham TV | https://mumt03.tangotv.in/Dsly5z3HSOHAMTV/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HSOHAMTV/index.m3u8 |
| Working | Same | SVBC 4 | https://player.mslivestream.net/mslive/13a2927187b9700ae7ea82d7841d5b68.sdp/playlist.m3u8 | https://player.mslivestream.net/mslive/13a2927187b9700ae7ea82d7841d5b68.sdp/playlist.m3u8 |
| Working | Same | Swastik TV | https://server.playontv.in/swastiktv/index.m3u8 | https://server.playontv.in/swastiktv/index.m3u8 |
| Working | Same | Total Bhakti | https://d34z4embz0hjf6.cloudfront.net/out/v1/d55b3323a9f142638f897378f0b526fe/index.m3u8 | https://d34z4embz0hjf6.cloudfront.net/out/v1/d55b3323a9f142638f897378f0b526fe/index.m3u8 |
| Working | Same | Vedic | https://mumt05.tangotv.in/87NeALx2VEDIC/index.m3u8 | https://mumt05.tangotv.in/87NeALx2VEDIC/index.m3u8 |

## Entertainment

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | Anjan TV | https://anjan.vstream.online/anjanorg/ngrp:anjan_hdall/playlist.m3u8 | https://anjan.vstream.online/anjanorg/ngrp:anjan_hdall/playlist.m3u8 |
| Working | Same | Apna Punjab TV | https://plus.gigabitcdn.net/live-stream/apna-punjab-H3sE/playlist.m3u8 | https://plus.gigabitcdn.net/live-stream/apna-punjab-H3sE/playlist.m3u8 |
| Working | Same | Aryan TV National | https://mumt04.tangotv.in/m18aqlK4ARYANTVNATIONAL/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4ARYANTVNATIONAL/index.m3u8 |
| Working | Same | BVG | https://mumt05.tangotv.in/87NeALx2BVG/index.m3u8 | https://mumt05.tangotv.in/87NeALx2BVG/index.m3u8 |
| Non-working | Same | Colors HD | http://66.102.126.10:8000/play/a00a/index.m3u8 | http://66.102.126.10:8000/play/a00a/index.m3u8 |
| Working | Same | Colors MENA HD | https://da86m1sqpm3o0.cloudfront.net/28072023/smil:colorsme.smil/playlist.m3u8 | https://da86m1sqpm3o0.cloudfront.net/28072023/smil:colorsme.smil/playlist.m3u8 |
| Working | Same | Colors Rishtey Americas | https://manatv.akamaized.net/090823/smil:ristheyamerica.smil/playlist.m3u8 | https://manatv.akamaized.net/090823/smil:ristheyamerica.smil/playlist.m3u8 |
| Working | Same | Dangal 2 | https://live-dangal2.akamaized.net/liveabr/playlist.m3u8 | https://live-dangal2.akamaized.net/liveabr/playlist.m3u8 |
| Working | Same | Dangal TV | https://live-dangal.akamaized.net/liveabr/playlist.m3u8 | https://live-dangal.akamaized.net/liveabr/playlist.m3u8 |
| Working | Same | DD Arun Prabha | https://d2lk5u59tns74c.cloudfront.net/out/v1/308556d9fd1246adb479ef012a39bbfe/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/308556d9fd1246adb479ef012a39bbfe/index.m3u8 |
| Working | Same | DD Bharati | https://cdn.pishow.tv/ott/live/10/master.m3u8 | https://cdn.pishow.tv/ott/live/10/master.m3u8 |
| Working | Same | DD Bihar | https://cdn.pishow.tv/ott/live/35/master.m3u8 | https://cdn.pishow.tv/ott/live/35/master.m3u8 |
| Working | Same | DD Chhattisgarh | https://cdn.pishow.tv/ott/live/15/master.m3u8 | https://cdn.pishow.tv/ott/live/15/master.m3u8 |
| Working | Same | DD Haryana | https://d2lk5u59tns74c.cloudfront.net/out/v1/950fc69666474351bde0a32b9600c804/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/950fc69666474351bde0a32b9600c804/index.m3u8 |
| Working | Same | DD Himachal Pradesh | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/afd2e335b0ba40eb9bdf1096118c6ede/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/afd2e335b0ba40eb9bdf1096118c6ede/index.m3u8 |
| Working | Same | DD Jharkhand | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/e8c3741f8c154d3185831f4e31777fb2/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/e8c3741f8c154d3185831f4e31777fb2/index.m3u8 |
| Working | Same | DD Kashir | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/8a59a828e80c49d0958925950cec0204/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/8a59a828e80c49d0958925950cec0204/index.m3u8 |
| Working | Same | DD Kisan | https://mumbai-edge.smartplaytv.in/DDKisan/index.m3u8 | https://mumbai-edge.smartplaytv.in/DDKisan/index.m3u8 |
| Working | Same | DD Madhya Pradesh | https://mumbai-edge.smartplaytv.in/ddmadhyapradesh/index.m3u8 | https://mumbai-edge.smartplaytv.in/ddmadhyapradesh/index.m3u8 |
| Working | Same | DD Manipur | https://d2lk5u59tns74c.cloudfront.net/out/v1/8b75afc6576f450e8f554b6c877681d2/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/8b75afc6576f450e8f554b6c877681d2/index.m3u8 |
| Working | Same | DD National | http://107.167.16.138/ddnational/index.m3u8?token=test | http://107.167.16.138/ddnational/index.m3u8?token=test |
| Working | Same | DD National HD | https://mumbai-edge.smartplaytv.in/DDNational/index.m3u8 | https://mumbai-edge.smartplaytv.in/DDNational/index.m3u8 |
| Working | Same | DD Rajasthan | https://cdn.pishow.tv/ott/live/34/master.m3u8 | https://cdn.pishow.tv/ott/live/34/master.m3u8 |
| Working | Same | DD Uttar Pradesh | https://cdn.pishow.tv/ott/live/36/master.m3u8 | https://cdn.pishow.tv/ott/live/36/master.m3u8 |
| Working | Same | DD Uttarakhand | https://cdn.pishow.tv/ott/live/17/master.m3u8 | https://cdn.pishow.tv/ott/live/17/master.m3u8 |
| Working | Same | Disha TV | https://d1msejlow1t3l4.cloudfront.net/fta/dishatv/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/dishatv/playlist.m3u8 |
| Working | Same | Diya TV | https://stream.diyatvinc.com/diya.m3u8 | https://stream.diyatvinc.com/diya.m3u8 |
| Working | Same | E 24 | https://mumt04.tangotv.in/m18aqlK4E24/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4E24/index.m3u8 |
| Non-working | Same | E-Vidya 4 | http://103.72.101.252:8080/live/406.m3u8 | http://103.72.101.252:8080/live/406.m3u8 |
| Non-working | Same | E-Vidya 5 | http://103.72.101.252:8080/live/407.m3u8 | http://103.72.101.252:8080/live/407.m3u8 |
| Non-working | Same | E-Vidya 6 | http://103.72.101.252:8080/live/408.m3u8 | http://103.72.101.252:8080/live/408.m3u8 |
| Non-working | Same | E-Vidya 7 | http://103.72.101.252:8080/live/404.m3u8 | http://103.72.101.252:8080/live/404.m3u8 |
| Non-working | Same | E-Vidya 8 | http://103.72.101.252:8080/live/409.m3u8 | http://103.72.101.252:8080/live/409.m3u8 |
| Non-working | Same | E-Vidya 9 | http://103.72.101.252:8080/live/410.m3u8 | http://103.72.101.252:8080/live/410.m3u8 |
| Non-working | Same | E-Vidya 10 | http://103.72.101.252:8080/live/411.m3u8 | http://103.72.101.252:8080/live/411.m3u8 |
| Non-working | Same | E-Vidya 11 | http://103.72.101.252:8080/live/1410.m3u8 | http://103.72.101.252:8080/live/1410.m3u8 |
| Non-working | Same | E-Vidya 12 | http://103.72.101.252:8080/live/1532.m3u8 | http://103.72.101.252:8080/live/1532.m3u8 |
| Working | Same | Epic Bharat | https://mumt06.tangotv.in/qYyB8fXVEPICTV/index.m3u8 | https://mumt06.tangotv.in/qYyB8fXVEPICTV/index.m3u8 |
| Working | Same | Epic Bharat Digital | https://cc-p1izg43bk7sj5.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-p1izg43bk7sj5/DIYC/PMSL/IN10/Nazara_IN_B/Nazara_IN_B.m3u8 | https://cc-p1izg43bk7sj5.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-p1izg43bk7sj5/DIYC/PMSL/IN10/Nazara_IN_B/Nazara_IN_B.m3u8 |
| Working | Same | Epic Crimes | https://cc-wsuyg2uxeak04.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-wsuyg2uxeak04/master.m3u8 | https://cc-wsuyg2uxeak04.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-wsuyg2uxeak04/master.m3u8 |
| Working | Same | Epic TV Digital | https://cc-czbq30x55knit.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-czbq30x55knit/DIYC/PMSL/IN10/Epic_TV_IN_B/Epic_TV_IN_B.m3u8 | https://cc-czbq30x55knit.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-czbq30x55knit/DIYC/PMSL/IN10/Epic_TV_IN_B/Epic_TV_IN_B.m3u8 |
| Working | Same | Gangaur TV | https://pbgangaur.wiseplayout.com/Gangaur/master.m3u8 | https://pbgangaur.wiseplayout.com/Gangaur/master.m3u8 |
| Working | Same | Gyandarshan | https://cdn.pishow.tv/ott/live/14/master.m3u8 | https://cdn.pishow.tv/ott/live/14/master.m3u8 |
| Working | Same | Gyandarshan HD | https://mumt05.tangotv.in/87NeALx2GYANDARSHAN/index.m3u8 | https://mumt05.tangotv.in/87NeALx2GYANDARSHAN/index.m3u8 |
| Working | Same | Hyder TV | https://cdn.live247stream.com/hyder/tv/playlist.m3u8 | https://cdn.live247stream.com/hyder/tv/playlist.m3u8 |
| Working | Same | Jan TV | https://d1msejlow1t3l4.cloudfront.net/fta/jantv/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/jantv/playlist.m3u8 |
| Non-working | Same | Jus Hindi | http://103.154.3.101:5001/live/960.m3u8 | http://103.154.3.101:5001/live/960.m3u8 |
| Non-working | Same | Jus One | http://103.154.3.101:5001/live/961.m3u8 | http://103.154.3.101:5001/live/961.m3u8 |
| Working | Same | Kaumudy TV | https://oqgdrkxby4rm-hls-live.5centscdn.com/kaumudytv/live.stream/playlist.m3u8 | https://oqgdrkxby4rm-hls-live.5centscdn.com/kaumudytv/live.stream/playlist.m3u8 |
| Working | Same | Mango | https://stmv6.voxtvhd.com.br/cinehindi/cinehindi/playlist.m3u8 | https://stmv6.voxtvhd.com.br/cinehindi/cinehindi/playlist.m3u8 |
| Non-working | Same | Manoranjan TV | http://103.213.31.109:90/ManoranjanTv/playlist.m3u8 | http://103.213.31.109:90/ManoranjanTv/playlist.m3u8 |
| Working | Same | Mh 1 Prime | https://streams.tangotv.in/MHONE/ORIGIN/index.m3u8 | https://streams.tangotv.in/MHONE/ORIGIN/index.m3u8 |
| Working | Same | MH One Dil Se | https://streams.tangotv.in/MHONEDILSE/ORIGIN/index.m3u8 | https://streams.tangotv.in/MHONEDILSE/ORIGIN/index.m3u8 |
| Working | Same | Network 10 | https://mumbai-edge.smartplaytv.in/Network10/index.m3u8 | https://mumbai-edge.smartplaytv.in/Network10/index.m3u8 |
| Working | Same | Prarthana Bhawan TV | https://mumt03.tangotv.in/Dsly5z3HPRATHANABHAWAN/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HPRATHANABHAWAN/index.m3u8 |
| Working | Same | Q TV | https://mumt05.tangotv.in/87NeALx2THEQ/index.m3u8 | https://mumt05.tangotv.in/87NeALx2THEQ/index.m3u8 |
| Working | Same | Raftaar Media | https://mumt04.tangotv.in/m18aqlK4RAFTAARMEDIA/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4RAFTAARMEDIA/index.m3u8 |
| Working | Same | Rongeen TV | https://server.thelegitpro.in/rongeentv/rongeentv/index.m3u8 | https://server.thelegitpro.in/rongeentv/rongeentv/index.m3u8 |
| Working | Same | Saam TV | https://cdn.pishow.tv/ott/live/437/master.m3u8 | https://cdn.pishow.tv/ott/live/437/master.m3u8 |
| Working | Same | Sansad TV 1 | https://playhls.media.nic.in/hls/live/lstv/lstv.m3u8 | https://playhls.media.nic.in/hls/live/lstv/lstv.m3u8 |
| Working | Same | Sansad TV 1 HD | https://d2lk5u59tns74c.cloudfront.net/out/v1/fff8f20221d5456e8922e689d71dedc3/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/fff8f20221d5456e8922e689d71dedc3/index.m3u8 |
| Working | Same | Sansad TV 2 | https://d2lk5u59tns74c.cloudfront.net/out/v1/e4182054dce340da9e0ff38b6b3658a4/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/e4182054dce340da9e0ff38b6b3658a4/index.m3u8 |
| Working | Same | Sansad TV 2 | https://cdn.pishow.tv/ott/live/39/master.m3u8 | https://cdn.pishow.tv/ott/live/39/master.m3u8 |
| Working | Same | Santvani Channel | https://cdn.pishow.tv/ott/live/475/master.m3u8 | https://cdn.pishow.tv/ott/live/475/master.m3u8 |
| Non-working | Same | Sarv Dharam Sangam | http://103.72.101.252:8080/live/972.m3u8 | http://103.72.101.252:8080/live/972.m3u8 |
| Working | Same | Sharnam TV | https://mumt06.tangotv.in/qYyB8fXVSHARNAMTV/index.m3u8 | https://mumt06.tangotv.in/qYyB8fXVSHARNAMTV/index.m3u8 |
| Working | Same | Shemaroo TV | https://airtelapp.shemaroo.com/shemarootv/smil:shemarootvadp.smil/playlist.m3u8 | https://airtelapp.shemaroo.com/shemarootv/smil:shemarootvadp.smil/playlist.m3u8 |
| Working | Same | Shemaroo Umang | https://airtelapp.shemaroo.com/shemarooumang/smil:shemarooumangadp.smil/playlist.m3u8 | https://airtelapp.shemaroo.com/shemarooumang/smil:shemarooumangadp.smil/playlist.m3u8 |
| Working | Same | Shubh TV | https://d2g1vdc6ozl2o8.cloudfront.net/out/v1/0a0dc7d7911b4fddbb4dfc963fdd4b9e/index.m3u8 | https://d2g1vdc6ozl2o8.cloudfront.net/out/v1/0a0dc7d7911b4fddbb4dfc963fdd4b9e/index.m3u8 |
| Working | Same | Sony Entertainment Television HD | http://38.96.178.205/SONYHD/index.m3u8 | http://38.96.178.205/SONYHD/index.m3u8 |
| Working | Same | Sony KAL Hindi | https://wurlsonypicturestv.global.transmit.live/hls/68deeb1c0238cda82df543dd/v1/spt_sonykal_1/lg_us/latest/main/hls/playlist.m3u8 | https://wurlsonypicturestv.global.transmit.live/hls/68deeb1c0238cda82df543dd/v1/spt_sonykal_1/lg_us/latest/main/hls/playlist.m3u8 |
| Working | Same | Sony Pal | https://cloudplay-sonyliv.pages.dev/pal.m3u8 | https://cloudplay-sonyliv.pages.dev/pal.m3u8 |
| Working | Same | Sony SAB HD | https://cloudplay-sonyliv.pages.dev/sabhd.m3u8 | https://cloudplay-sonyliv.pages.dev/sabhd.m3u8 |
| Working | Same | StarPlus HD (1080i) | http://202.70.146.135:8000/play/a009/index.m3u8 | http://202.70.146.135:8000/play/a009/index.m3u8 |
| Non-working | Same | Swayam Prabha 1 | http://103.72.101.252:8080/live/980.m3u8 | http://103.72.101.252:8080/live/980.m3u8 |
| Non-working | Same | Swayam Prabha 3 | http://103.72.101.252:8080/live/982.m3u8 | http://103.72.101.252:8080/live/982.m3u8 |
| Non-working | Same | Swayam Prabha 4 | http://103.72.101.252:8080/live/984.m3u8 | http://103.72.101.252:8080/live/984.m3u8 |
| Non-working | Same | Swayam Prabha 5 | http://103.72.101.252:8080/live/986.m3u8 | http://103.72.101.252:8080/live/986.m3u8 |
| Non-working | Same | Swayam Prabha 6 | http://103.72.101.252:8080/live/987.m3u8 | http://103.72.101.252:8080/live/987.m3u8 |
| Non-working | Same | Swayam Prabha 7 | http://103.72.101.252:8080/live/985.m3u8 | http://103.72.101.252:8080/live/985.m3u8 |
| Non-working | Same | Swayam Prabha 8 | http://103.72.101.252:8080/live/983.m3u8 | http://103.72.101.252:8080/live/983.m3u8 |
| Non-working | Same | Swayam Prabha 9 | http://103.72.101.252:8080/live/988.m3u8 | http://103.72.101.252:8080/live/988.m3u8 |
| Non-working | Same | Swayam Prabha 10 | http://103.72.101.252:8080/live/989.m3u8 | http://103.72.101.252:8080/live/989.m3u8 |
| Non-working | Same | Swayam Prabha 11 | http://103.72.101.252:8080/live/990.m3u8 | http://103.72.101.252:8080/live/990.m3u8 |
| Non-working | Same | Swayam Prabha 12 | http://103.72.101.252:8080/live/991.m3u8 | http://103.72.101.252:8080/live/991.m3u8 |
| Non-working | Same | Swayam Prabha 13 | http://103.72.101.252:8080/live/992.m3u8 | http://103.72.101.252:8080/live/992.m3u8 |
| Non-working | Same | Swayam Prabha 14 | http://103.72.101.252:8080/live/993.m3u8 | http://103.72.101.252:8080/live/993.m3u8 |
| Non-working | Same | Swayam Prabha 15 | http://103.72.101.252:8080/live/995.m3u8 | http://103.72.101.252:8080/live/995.m3u8 |
| Non-working | Same | Swayam Prabha 16 | http://103.72.101.252:8080/live/994.m3u8 | http://103.72.101.252:8080/live/994.m3u8 |
| Non-working | Same | Swayam Prabha 17 | http://103.72.101.252:8080/live/996.m3u8 | http://103.72.101.252:8080/live/996.m3u8 |
| Non-working | Same | Swayam Prabha 18 | http://103.72.101.252:8080/live/999.m3u8 | http://103.72.101.252:8080/live/999.m3u8 |
| Non-working | Same | Swayam Prabha 19 | http://103.72.101.252:8080/live/401.m3u8 | http://103.72.101.252:8080/live/401.m3u8 |
| Non-working | Same | Swayam Prabha 20 | http://103.72.101.252:8080/live/403.m3u8 | http://103.72.101.252:8080/live/403.m3u8 |
| Non-working | Same | Swayam Prabha 21 | http://103.72.101.252:8080/live/997.m3u8 | http://103.72.101.252:8080/live/997.m3u8 |
| Non-working | Same | Swayam Prabha 22 | http://103.72.101.252:8080/live/998.m3u8 | http://103.72.101.252:8080/live/998.m3u8 |
| Working | Same | Taaza TV | https://live.we2live.in/taazatv/live/playlist.m3u8 | https://live.we2live.in/taazatv/live/playlist.m3u8 |
| Working | Same | TAG TV (1080p) | http://cdn11.live247stream.com/tag/tv/playlist.m3u8 | http://cdn11.live247stream.com/tag/tv/playlist.m3u8 |
| Working | Same | TBN TV (720p) | https://live.suricloud.com/hls/tbntv/index.m3u8 | https://live.suricloud.com/hls/tbntv/index.m3u8 |
| Working | Same | Tehzeeb TV | https://cdn.pishow.tv/ott/live/239/master.m3u8 | https://cdn.pishow.tv/ott/live/239/master.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Undefined",The Q India | http://103.175.73.12:8080/live/25/25_0.m3u8 | http://103.175.73.12:8080/live/25/25_0.m3u8 |
| Working | Same | Total TV Haryana | https://cdn.pishow.tv/ott/live/1522/master.m3u8 | https://cdn.pishow.tv/ott/live/1522/master.m3u8 |
| Non-working | Same | TV2 | https://live.mana2.my/Tv2/index.m3u8?auth_key=1745177833-e4f0090e3d3b4ed1b2b4f5df87a24d34-0-d43f8be1101f9bb00363d62de6514e4d&token=1745177833-e4f0090e3d3b4ed1b2b4f5df87a24d34-0-d43f8be1101f9bb00363d62de6514e4d | https://live.mana2.my/Tv2/index.m3u8?auth_key=1745177833-e4f0090e3d3b4ed1b2b4f5df87a24d34-0-d43f8be1101f9bb00363d62de6514e4d&token=1745177833-e4f0090e3d3b4ed1b2b4f5df87a24d34-0-d43f8be1101f9bb00363d62de6514e4d |
| Working | Same | Utsav Bharat | https://d1taaads3ztvmu.cloudfront.net/120723/smil:lifeokuk.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://d1taaads3ztvmu.cloudfront.net/120723/smil:lifeokuk.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | Utsav Plus | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/gb/YuppTV/UtsavPlus.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/gb/YuppTV/UtsavPlus.m3u8 |
| Non-working | Same | Vande Gujarat 1 | http://103.72.101.252:8080/live/1069.m3u8 | http://103.72.101.252:8080/live/1069.m3u8 |
| Non-working | Same | Vande Gujarat 2 | http://103.72.101.252:8080/live/1070.m3u8 | http://103.72.101.252:8080/live/1070.m3u8 |
| Non-working | Same | Vande Gujarat 3 | http://103.72.101.252:8080/live/1082.m3u8 | http://103.72.101.252:8080/live/1082.m3u8 |
| Non-working | Same | Vande Gujarat 4 | http://103.72.101.252:8080/live/1071.m3u8 | http://103.72.101.252:8080/live/1071.m3u8 |
| Non-working | Same | Vande Gujarat 5 | http://103.72.101.252:8080/live/1083.m3u8 | http://103.72.101.252:8080/live/1083.m3u8 |
| Non-working | Same | Vande Gujarat 6 | http://103.72.101.252:8080/live/1084.m3u8 | http://103.72.101.252:8080/live/1084.m3u8 |
| Non-working | Same | Vande Gujarat 7 | http://103.72.101.252:8080/live/1085.m3u8 | http://103.72.101.252:8080/live/1085.m3u8 |
| Non-working | Same | Vande Gujarat 8 | http://103.72.101.252:8080/live/1086.m3u8 | http://103.72.101.252:8080/live/1086.m3u8 |
| Non-working | Same | Vande Gujarat 9 | http://103.72.101.252:8080/live/1087.m3u8 | http://103.72.101.252:8080/live/1087.m3u8 |
| Non-working | Same | Vande Gujarat 10 | http://103.72.101.252:8080/live/1088.m3u8 | http://103.72.101.252:8080/live/1088.m3u8 |
| Non-working | Same | Vande Gujarat 11 | http://103.72.101.252:8080/live/1089.m3u8 | http://103.72.101.252:8080/live/1089.m3u8 |
| Non-working | Same | Vande Gujarat 12 | http://103.72.101.252:8080/live/1090.m3u8 | http://103.72.101.252:8080/live/1090.m3u8 |
| Non-working | Same | Vande Gujarat 13 | http://103.72.101.252:8080/live/1091.m3u8 | http://103.72.101.252:8080/live/1091.m3u8 |
| Non-working | Same | Vande Gujarat 14 | http://103.72.101.252:8080/live/1092.m3u8 | http://103.72.101.252:8080/live/1092.m3u8 |
| Non-working | Same | Vande Gujarat 15 | http://103.72.101.252:8080/live/1093.m3u8 | http://103.72.101.252:8080/live/1093.m3u8 |
| Non-working | Same | Vande Gujarat 16 | http://103.72.101.252:8080/live/1094.m3u8 | http://103.72.101.252:8080/live/1094.m3u8 |
| Working | Same | VTU | https://lbgo.bozztv.com/ssh101/ssh101/afghantheatretv/playlist.m3u8 | https://lbgo.bozztv.com/ssh101/ssh101/afghantheatretv/playlist.m3u8 |
| Working | Same | Weatherspy | https://jukin-weatherspy-2-in.samsung.wurl.tv/playlist.m3u8 | https://jukin-weatherspy-2-in.samsung.wurl.tv/playlist.m3u8 |
| Non-working | Same | Zee Comedy Nation | https://amg00862-amg00862c5-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c5-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c5-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c5-amgplt0173/playlist.m3u8 |
| Non-working | Same | Zee Dil Se | https://amg00862-amg00862c6-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c6-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c6-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c6-amgplt0173/playlist.m3u8 |
| Non-working | Same | Zee Horror Nights | https://amg00862-amg00862c7-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c7-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c7-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c7-amgplt0173/playlist.m3u8 |
| Working | Same | Zee TV HD (720p) | http://41.205.93.154/ZEE-TV/index.m3u8 | http://41.205.93.154/ZEE-TV/index.m3u8 |
| Non-working | Same | Captain | https://mumbai-edge.smartplaytv.in/captain/index.m3u8 | https://mumbai-edge.smartplaytv.in/captain/index.m3u8 |
| Working | Same | Manoranjan Prime | https://mumt06.tangotv.in/qYyB8fXVMANORANJANPRIME/index.m3u8 | https://mumt06.tangotv.in/qYyB8fXVMANORANJANPRIME/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Entertainment",Pasand TV | http://103.175.73.12:8080/live/708/master.m3u8 | http://103.175.73.12:8080/live/708/master.m3u8 |
| Working | Same | DD India | https://mumbai-edge.smartplaytv.in/DDIndia/index.m3u8 | https://mumbai-edge.smartplaytv.in/DDIndia/index.m3u8 |

## Lifestyle

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | Food Food | https://mumt03.tangotv.in/Dsly5z3HFOODFOOD/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HFOODFOOD/index.m3u8 |
| Non-working | Same | Travelxp 4K HDR (2160p) | https://deltatesttatasky.akamaized.net/out/i/968284.m3u8 | https://deltatesttatasky.akamaized.net/out/i/968284.m3u8 |
| Working | Same | Travelxp HD (1080p) | https://amg00416-amg00416c9-samsung-in-4882.playouts.now.amagi.tv/playlist/amg00416-travelxp-travelxphd-samsungin/playlist.m3u8 | https://amg00416-amg00416c9-samsung-in-4882.playouts.now.amagi.tv/playlist/amg00416-travelxp-travelxphd-samsungin/playlist.m3u8 |
| Non-working | Same | Zee Zest HD | http://103.72.101.252:8080/live/2757.m3u8 | http://103.72.101.252:8080/live/2757.m3u8 |

## Movie

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | &TV HD | http://202.70.146.135:8000/play/a06c/index.m3u8 | http://202.70.146.135:8000/play/a06c/index.m3u8 |
| Non-working | Same | &TV International | https://amg01117-amg01117c1-amgplt0029.playout.now3.amagi.tv/playlist/amg01117-amg01117c1-amgplt0029/playlist.m3u8 | https://amg01117-amg01117c1-amgplt0029.playout.now3.amagi.tv/playlist/amg01117-amg01117c1-amgplt0029/playlist.m3u8 |
| Non-working | Same | &xplor HD (1080p) | http://dksmedia.tv/play/live.php?mac=00:1A:79:B6:60:3D&stream=209743&extension=ts&play_token=mR7FwO88sY | http://dksmedia.tv/play/live.php?mac=00:1A:79:B6:60:3D&stream=209743&extension=ts&play_token=mR7FwO88sY |
| Working | Same | All Time Movies | https://tvsen6.aynaott.com/a2cKGQtB/index.m3u8 | https://tvsen6.aynaott.com/a2cKGQtB/index.m3u8 |
| Working | Same | B4U Kadak | https://streams.tangotv.in/B4UKADAK/ORIGIN/index.m3u8 | https://streams.tangotv.in/B4UKADAK/ORIGIN/index.m3u8 |
| Working | Same | B4U Movies | https://streams.tangotv.in/B4UMOVIES/ORIGIN/index.m3u8 | https://streams.tangotv.in/B4UMOVIES/ORIGIN/index.m3u8 |
| Working | Same | Bollygold | https://jmp2.uk/stvp-IN4000600Q | https://jmp2.uk/stvp-IN4000600Q |
| Non-working | Same | like Gecko) Chrome/130.0.0.0 Safari/537.36 VLC/3.0.18 LibVLC/3.0.18" group-title="Classic;Movies",Bollywood Classic Romania | https://flash1.bogulus1.cfd/boly/usergenr9j8s2t.m3u8 | https://flash1.bogulus1.cfd/boly/usergenr9j8s2t.m3u8 |
| Working | Same | Bollywood HD Russia | https://xykt-fix.github.io/cinerama_edge01/hls/BOLLYWOOD_RU/Movie009.m3u8 | https://xykt-fix.github.io/cinerama_edge01/hls/BOLLYWOOD_RU/Movie009.m3u8 |
| Working | Same | Colors Cineplex Bollywood | http://202.70.146.135:8000/play/a058/index.m3u8 | http://202.70.146.135:8000/play/a058/index.m3u8 |
| Working | Same | Goldmines | https://streams.tangotv.in/GOLDMINES/ORIGIN/index.m3u8 | https://streams.tangotv.in/GOLDMINES/ORIGIN/index.m3u8 |
| Working | Same | Goldmines 2 | https://mumt03.tangotv.in/Dsly5z3HGOLDMINES2/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HGOLDMINES2/index.m3u8 |
| Working | Same | Goldmines Action | https://mumt03.tangotv.in/Dsly5z3HGOLDMINESACTION/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HGOLDMINESACTION/index.m3u8 |
| Working | Same | Goldmines Bollywood | https://mumt03.tangotv.in/Dsly5z3HGOLDMINESBOLLYWOOD/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HGOLDMINESBOLLYWOOD/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Movies",Goldmines Movies | http://103.175.73.12:8080/live/51/51_0.m3u8 | http://103.175.73.12:8080/live/51/51_0.m3u8 |
| Working | Same | Maha Movie | https://cdn.pishow.tv/ott/live/10007/master.m3u8 | https://cdn.pishow.tv/ott/live/10007/master.m3u8 |
| Working | Same | Manoranjan Grand | https://cdn.pishow.tv/ott/live/1011/master.m3u8 | https://cdn.pishow.tv/ott/live/1011/master.m3u8 |
| Working | Same | MBC Bollywood (1080p) | https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-bollywood/546eb40d7dcf9a209255dd2496903764/index.m3u8 | https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-bollywood/546eb40d7dcf9a209255dd2496903764/index.m3u8 |
| Working | Same | MH One Movies | https://mumt03.tangotv.in/Dsly5z3HMHONEMOVIE/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HMHONEMOVIE/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Movies",MoviePlex | http://103.175.73.12:8080/live/583/master.m3u8 | http://103.175.73.12:8080/live/583/master.m3u8 |
| Working | Same | NH BollyFlix | https://jmp2.uk/stvp-IN46000140Q | https://jmp2.uk/stvp-IN46000140Q |
| Working | Same | NH BollyGold | https://0dc330e6408b4c3b9ac31fd37b121368.mediatailor.ap-south-1.amazonaws.com/v1/master/d367f9b863a7a04827f71ecab4cbeeb11f78a827/nh-bollygold-airtel/playlist.m3u8 | https://0dc330e6408b4c3b9ac31fd37b121368.mediatailor.ap-south-1.amazonaws.com/v1/master/d367f9b863a7a04827f71ecab4cbeeb11f78a827/nh-bollygold-airtel/playlist.m3u8 |
| Working | Same | Pocket Films | https://vglivessai.akamaized.net/sg/v1/manifest/611d79b11b77e2f571934fd80ca1413453772ac7/b8ada260-bb81-472b-b7c1-3a79213a84b8/e02a0ce5-6c42-4cca-bb53-e5cfecff74a9/0.m3u8 | https://vglivessai.akamaized.net/sg/v1/manifest/611d79b11b77e2f571934fd80ca1413453772ac7/b8ada260-bb81-472b-b7c1-3a79213a84b8/e02a0ce5-6c42-4cca-bb53-e5cfecff74a9/0.m3u8 |
| Non-working | Same | Shemaroo Filmi Gaane | http://103.213.31.109:90/ShemarooFilmiGaane/playlist.m3u8 | http://103.213.31.109:90/ShemarooFilmiGaane/playlist.m3u8 |
| Working | Same | Shemaroo Josh | https://airtelapp.shemaroo.com/shemarooChumbakTV/smil:shemarooChumbakTVadp.smil/playlist.m3u8 | https://airtelapp.shemaroo.com/shemarooChumbakTV/smil:shemarooChumbakTVadp.smil/playlist.m3u8 |
| Working | Same | Shubh Cinema TV | https://d393sxaxig6bax.cloudfront.net/out/v1/589cf2cf44bf42bb941e817a2240d62e/index.m3u8 | https://d393sxaxig6bax.cloudfront.net/out/v1/589cf2cf44bf42bb941e817a2240d62e/index.m3u8 |
| Working | Same | Sony Max | https://cloudplay-sonyliv.pages.dev/max.m3u8 | https://cloudplay-sonyliv.pages.dev/max.m3u8 |
| Working | Same | Sony Max 2 | https://cloudplay-sonyliv.pages.dev/max2.m3u8 | https://cloudplay-sonyliv.pages.dev/max2.m3u8 |
| Working | Same | Sony Max HD | https://cloudplay-sonyliv.pages.dev/maxhd.m3u8 | https://cloudplay-sonyliv.pages.dev/maxhd.m3u8 |
| Working | Same | Sony Pix HD | https://cloudplay-sonyliv.pages.dev/pixhd.m3u8 | https://cloudplay-sonyliv.pages.dev/pixhd.m3u8 |
| Working | Same | Sony Wah | https://cloudplay-sonyliv.pages.dev/wah.m3u8 | https://cloudplay-sonyliv.pages.dev/wah.m3u8 |
| Working | Same | South Station | https://cc-yw7ztecy8do3q.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-yw7ztecy8do3q/SS_IN.m3u8 | https://cc-yw7ztecy8do3q.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-yw7ztecy8do3q/SS_IN.m3u8 |
| Non-working | Same | Star Gold 2 | http://107.167.16.138/stargold2/index.m3u8?token=test | http://107.167.16.138/stargold2/index.m3u8?token=test |
| Non-working | Same | Star Gold 2 HD | http://66.102.126.10:8000/play/a077/index.m3u8 | http://66.102.126.10:8000/play/a077/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/129.0.0.0 Safari/537.36" group-title="Movies",Star Gold Thrills | http://103.253.18.58:8000/play/a00o | http://103.253.18.58:8000/play/a00o |
| Working | Same | The Movie Club | https://sis-global.prod.samsungtv.plus/v1/tvpprd/sc-mp2ar4ca425xo.m3u8 | https://sis-global.prod.samsungtv.plus/v1/tvpprd/sc-mp2ar4ca425xo.m3u8 |
| Working | Same | The Movie Club +2 | https://d3gnyty2vddhsg.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/pb-ytipwjqub3kf8/TMC2_IN.m3u8?ads.ads_cdn=cf&ads.cdn=cf | https://d3gnyty2vddhsg.cloudfront.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/pb-ytipwjqub3kf8/TMC2_IN.m3u8?ads.ads_cdn=cf&ads.cdn=cf |
| Non-working | Same | Zee Action | http://107.167.16.138/zeeaction/index.m3u8?token=test | http://107.167.16.138/zeeaction/index.m3u8?token=test |
| Non-working | Same | Zee Cine Classic | https://amg00862-amg00862c8-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c8-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c8-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c8-amgplt0173/playlist.m3u8 |
| Working | Same | Zee Cinema | https://d1g8wgjurz8via.cloudfront.net/bpk-tv/NGCHD/default/NGCHD.m3u8 | https://d1g8wgjurz8via.cloudfront.net/bpk-tv/NGCHD/default/NGCHD.m3u8 |
| Working | Same | Zee Cinema APAC | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/sg/YuppTV/ZeeCinemaAPAC.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/sg/YuppTV/ZeeCinemaAPAC.m3u8 |
| Non-working | Same | Zee Cinema ME (432p) | https://ev-eu-hw-fast-mpd.starzplayarabia.com/Zee_Cinema/dash/drm/index.mpd | https://ev-eu-hw-fast-mpd.starzplayarabia.com/Zee_Cinema/dash/drm/index.mpd |
| Non-working | Same | Zee Cinemalu HD | https://mumbai-edge.smartplaytv.in/ZeeCinemaluHD/index.m3u8 | https://mumbai-edge.smartplaytv.in/ZeeCinemaluHD/index.m3u8 |
| Non-working | Same | Zee Classic | http://103.72.101.252:8080/live/1691.m3u8 | http://103.72.101.252:8080/live/1691.m3u8 |
| Non-working | Same | Zee South Flix | https://amg00862-amg00862c9-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c9-amgplt0173/playlist.m3u8 | https://amg00862-amg00862c9-amgplt0173.playout.now3.amagi.tv/playlist/amg00862-amg00862c9-amgplt0173/playlist.m3u8 |
| Working | Same | B4U Bhojpuri | https://cdnb4u.wiseplayout.com/B4U_Bhojpuri/master.m3u8 | https://cdnb4u.wiseplayout.com/B4U_Bhojpuri/master.m3u8 |
| Working | Same | Bhojpuri Cinema | https://live-bhojpuri.akamaized.net/liveabr/playlist.m3u8 | https://live-bhojpuri.akamaized.net/liveabr/playlist.m3u8 |
| Working | Same | Epic Bhojpuri | https://mumt01.tangotv.in/O5aw8Zn3EPICBHOJPURI/index.m3u8 | https://mumt01.tangotv.in/O5aw8Zn3EPICBHOJPURI/index.m3u8 |
| Working | Same | Epic Bhojpuri Digital | https://cc-8hy4a26pz2uos.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-8hy4a26pz2uos/playlist.m3u8 | https://cc-8hy4a26pz2uos.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-8hy4a26pz2uos/playlist.m3u8 |
| Working | Same | Oscar Movies Bhojpuri | https://cdn.pishow.tv/ott/live/233/master.m3u8 | https://cdn.pishow.tv/ott/live/233/master.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Movies",Zee Biskope | http://103.175.73.12:8080/live/347/master.m3u8 | http://103.175.73.12:8080/live/347/master.m3u8 |

## Music

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | 9X Jalwa | https://wiselp.wiseplayout.com/9X_Jalwa/master.m3u8 | https://wiselp.wiseplayout.com/9X_Jalwa/master.m3u8 |
| Working | Same | 9XM | https://9xjio.wiseplayout.com/9XM/master.m3u8 | https://9xjio.wiseplayout.com/9XM/master.m3u8 |
| Working | Same | Andy Haryana | https://mumt03.tangotv.in/Dsly5z3HANDYHARYANA/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HANDYHARYANA/index.m3u8 |
| Working | Same | B4U Music | https://cdn.pishow.tv/ott/live/415/master.m3u8 | https://cdn.pishow.tv/ott/live/415/master.m3u8 |
| Working | Same | Balle Balle | https://streams.tangotv.in/BALLEBALLE/ORIGIN/index.m3u8 | https://streams.tangotv.in/BALLEBALLE/ORIGIN/index.m3u8 |
| Working | Same | Balle Balle HD | https://mcncdndigital.com/balleballetv/index.m3u8 | https://mcncdndigital.com/balleballetv/index.m3u8 |
| Working | Same | Boogle Bollywood | https://yuppnimrestreammum.akamaized.net/181224/smil:bogglebollywood.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b | https://yuppnimrestreammum.akamaized.net/181224/smil:bogglebollywood.smil/playlist.m3u8?hdnts=st=1735898689~exp=1835898688~acl=*~hmac=f5fe24724fe05481e3841f9eb5ab8efdee0a3dd83645ae9dcf45703f525bab7b |
| Working | Same | Deewana HD | https://live20.bozztv.com/giatvplayout7/giatv-209592/index.m3u8 | https://live20.bozztv.com/giatvplayout7/giatv-209592/index.m3u8 |
| Working | Same | Dhamaal | http://107.167.16.138/dhamaal/index.m3u8?token=test | http://107.167.16.138/dhamaal/index.m3u8?token=test |
| Working | Same | Epic Music | https://mumt04.tangotv.in/m18aqlK4EPICMUSIC/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4EPICMUSIC/index.m3u8 |
| Working | Same | Epic Music Digital | https://cc-3cyxq80qusspd.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-3cyxq80qusspd/playlist.m3u8 | https://cc-3cyxq80qusspd.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-3cyxq80qusspd/playlist.m3u8 |
| Working | Same | Insync | https://mumt04.tangotv.in/m18aqlK4INSYNC/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4INSYNC/index.m3u8 |
| Working | Same | Mastiii | https://mumbai-edge.smartplaytv.in/MastiMusic/index.m3u8 | https://mumbai-edge.smartplaytv.in/MastiMusic/index.m3u8 |
| Working | Same | like Gecko) Chrome/130.0.0.0 Safari/537.36" group-title="Entertainment",MTV | https://da86m1sqpm3o0.cloudfront.net/28072023/smil:mtvindia.smil/playlist.m3u8 | https://da86m1sqpm3o0.cloudfront.net/28072023/smil:mtvindia.smil/playlist.m3u8 |
| Non-working | Same | like Gecko) Chrome/130.0.0.0 Safari/537.36" group-title="Entertainment",MTV HD | https://maamusic.keralive.workers.dev/out/v1/a797c00cba954265ba781f92a57e2cf5/index.m3u8 | https://maamusic.keralive.workers.dev/out/v1/a797c00cba954265ba781f92a57e2cf5/index.m3u8 |
| Working | Same | Music India | https://streams.tangotv.in/MUSICINDIA/ORIGIN/index.m3u8 | https://streams.tangotv.in/MUSICINDIA/ORIGIN/index.m3u8 |
| Working | Same | NH BollyRaga | https://jmp2.uk/stvp-IN460001373 | https://jmp2.uk/stvp-IN460001373 |
| Non-working | Same | Songdew TV | http://103.72.101.252:8080/live/1411.m3u8 | http://103.72.101.252:8080/live/1411.m3u8 |
| Working | Same | Steelbird Music (720p) | https://cdn2.in/SteelbirdMusicTVhls/live.m3u8 | https://cdn2.in/SteelbirdMusicTVhls/live.m3u8 |
| Working | Same | YRF Music | https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg01412-xiaomiasia-yrfmusic-xiaomi/playlist.m3u8 | https://cdn-uw2-prod.tsv2.amagi.tv/linear/amg01412-xiaomiasia-yrfmusic-xiaomi/playlist.m3u8 |
| Non-working | Same | Zing! | http://103.72.101.252:8080/live/585.m3u8 | http://103.72.101.252:8080/live/585.m3u8 |
| Working | Same | Zoom | https://dai.google.com/linear/hls/event/JCAm25qkRXiKcK1AJMlvKQ/master.m3u8 | https://dai.google.com/linear/hls/event/JCAm25qkRXiKcK1AJMlvKQ/master.m3u8 |
| Non-working | Same | Zoom Global | https://d14c63magvk61v.cloudfront.net/strm/channels/zoom/master.m3u8 | https://d14c63magvk61v.cloudfront.net/strm/channels/zoom/master.m3u8 |
| Non-working | Same | Sangeet Bhojpuri | http://103.213.31.109:90/SangeetBhojpuri/playlist.m3u8 | http://103.213.31.109:90/SangeetBhojpuri/playlist.m3u8 |
| Working | Same | 7S Music | https://cdn.pishow.tv/ott/live/1257/master.m3u8 | https://cdn.pishow.tv/ott/live/1257/master.m3u8 |
| Working | Same | 9X Jhakaas | https://amg01281-9xmediapvtltd-9xjhakaas-samsungin-ci2cs.amagi.tv/playlist/amg01281-9xmediapvtltd-9xjhakaas-samsungin/playlist.m3u8 | https://amg01281-9xmediapvtltd-9xjhakaas-samsungin-ci2cs.amagi.tv/playlist/amg01281-9xmediapvtltd-9xjhakaas-samsungin/playlist.m3u8 |
| Working | Same | 9X Tashan | https://amg01281-9xmediapvtltd-9xtashan-samsungin-xz1sd.amagi.tv/playlist/amg01281-9xmediapvtltd-9xtashan-samsungin/playlist.m3u8 | https://amg01281-9xmediapvtltd-9xtashan-samsungin-xz1sd.amagi.tv/playlist/amg01281-9xmediapvtltd-9xtashan-samsungin/playlist.m3u8 |
| Working | Same | Dhoom Music | https://cdn.pishow.tv/ott/live/1456/master.m3u8 | https://cdn.pishow.tv/ott/live/1456/master.m3u8 |
| Non-working | Same | ETV Music | https://mumbai-edge.smartplaytv.in/ETVABHIRUCHI/index.m3u8 | https://mumbai-edge.smartplaytv.in/ETVABHIRUCHI/index.m3u8 |
| Working | Same | Mh 1 Music | https://livestream.jswk.online/playlisttest/live/playlist.m3u8 | https://livestream.jswk.online/playlisttest/live/playlist.m3u8 |
| Working | Same | PTC Music | https://d2lk5u59tns74c.cloudfront.net/out/v1/f913cf893c594f73b114216e74a2efbc/index.m3u8 | https://d2lk5u59tns74c.cloudfront.net/out/v1/f913cf893c594f73b114216e74a2efbc/index.m3u8 |
| Working | Same | Public Music | https://mumt04.tangotv.in/m18aqlK4PUBLICMUSIC/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4PUBLICMUSIC/index.m3u8 |
| Working | Same | Tarang Music | https://livetv.tarangplus.in/tarangmusic-origin/live/playlist.m3u8 | https://livetv.tarangplus.in/tarangmusic-origin/live/playlist.m3u8 |
| Non-working | Same | ZB Music | https://server.zillarbarta.com/zbmusic/index.m3u8 | https://server.zillarbarta.com/zbmusic/index.m3u8 |

## News

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | 22Scope News | https://thelegitpro.in/HDlive/22scope/index.fmp4.m3u8 | https://thelegitpro.in/HDlive/22scope/index.fmp4.m3u8 |
| Working | Same | Aaj Ki Khabar | https://stream.ottlive.co.in/aajkikhabar/index.m3u8 | https://stream.ottlive.co.in/aajkikhabar/index.m3u8 |
| Non-working | Same | Aaj Tak | http://103.213.31.109:90/AajtakHD/playlist.m3u8 | http://103.213.31.109:90/AajtakHD/playlist.m3u8 |
| Working | Same | Aaj Tak HD | https://feeds.intoday.in/aajtak/api/aajtakhd/master.m3u8 | https://feeds.intoday.in/aajtak/api/aajtakhd/master.m3u8 |
| Working | Same | ABP Ganga | https://d2l4ar6y3mrs4k.cloudfront.net/live-streaming/ganga-livetv/master.m3u8 | https://d2l4ar6y3mrs4k.cloudfront.net/live-streaming/ganga-livetv/master.m3u8 |
| Working | Same | ABP News | https://d1rc86nwwc9fag.cloudfront.net/vglive-sk-472500/abpnews/master.m3u8 | https://d1rc86nwwc9fag.cloudfront.net/vglive-sk-472500/abpnews/master.m3u8 |
| Working | Same | AmarUjala | https://amarujala.ottlive.co.in/amarujala/index.m3u8 | https://amarujala.ottlive.co.in/amarujala/index.m3u8 |
| Working | Same | ANB News | https://server.livelegitpro.in:9899/anbnews/anbnews/index.m3u8 | https://server.livelegitpro.in:9899/anbnews/anbnews/index.m3u8 |
| Working | Same | APN | https://mumt01.tangotv.in/O5aw8Zn3APN/index.m3u8 | https://mumt01.tangotv.in/O5aw8Zn3APN/index.m3u8 |
| Working | Same | Argus News | https://mumt05.tangotv.in/87NeALx2ARGUSNEWS/index.m3u8 | https://mumt05.tangotv.in/87NeALx2ARGUSNEWS/index.m3u8 |
| Working | Same | Asian News | https://stream.ottlive.co.in/asiannews/index.m3u8 | https://stream.ottlive.co.in/asiannews/index.m3u8 |
| Working | Same | Awaaz India TV (720p) | https://awaazindia.livebox.co.in/AwaazIndaTVhls/Live.m3u8 | https://awaazindia.livebox.co.in/AwaazIndaTVhls/Live.m3u8 |
| Non-working | Same | Bansal News | https://8yzmq2gbdvax-hls-live.wmncdn.net/bansalnewstv1/live1.stream/playlist.m3u8 | https://8yzmq2gbdvax-hls-live.wmncdn.net/bansalnewstv1/live1.stream/playlist.m3u8 |
| Working | Same | Bharat24 | https://cdn.ottlive.co.in/bharat24/index.m3u8 | https://cdn.ottlive.co.in/bharat24/index.m3u8 |
| Working | Same | Bharat Samachar | https://mumt03.tangotv.in/Dsly5z3HBHARATSAMACHAR/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HBHARATSAMACHAR/index.m3u8 |
| Working | Same | Cnews Bharat | https://legitpro.co.in/cnews/cnews/index.fmp4.m3u8 | https://legitpro.co.in/cnews/cnews/index.fmp4.m3u8 |
| Working | Same | DD News | https://mumbai-edge.smartplaytv.in/DDNews/index.m3u8 | https://mumbai-edge.smartplaytv.in/DDNews/index.m3u8 |
| Working | Same | DD News HD | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/0811cd8c37ca4c409d5385a6cd2fa18b/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/0811cd8c37ca4c409d5385a6cd2fa18b/index.m3u8 |
| Working | Same | First India News | https://mumt03.tangotv.in/Dsly5z3H1STINDIANEWS/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3H1STINDIANEWS/index.m3u8 |
| Working | Same | Good News Today | https://aajtaklive.vgcdn.net/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/3196cced-ce29-4219-9809-f07ccdaa02b9/vglive-sk-848805/master.m3u8 | https://aajtaklive.vgcdn.net/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/3196cced-ce29-4219-9809-f07ccdaa02b9/vglive-sk-848805/master.m3u8 |
| Working | Same | Hindi Khabar | https://stream.ottlive.co.in/hindikhabar/index.m3u8 | https://stream.ottlive.co.in/hindikhabar/index.m3u8 |
| Working | Same | HNN 24x7 | https://ott.livelegitpro.in:9899/hnnnews/hnnnews/index.m3u8 | https://ott.livelegitpro.in:9899/hnnnews/hnnnews/index.m3u8 |
| Working | Same | IBC 24 | https://mumt05.tangotv.in/87NeALx2IBC24/index.m3u8 | https://mumt05.tangotv.in/87NeALx2IBC24/index.m3u8 |
| Non-working | Same | Ind 24 | https://mumt06.tangotv.in/qYyB8fXVIND24/index.m3u8 | https://mumt06.tangotv.in/qYyB8fXVIND24/index.m3u8 |
| Working | Same | India Daily Live | https://indiadaily.ottlive.co.in/indiadailylive/index.m3u8 | https://indiadaily.ottlive.co.in/indiadailylive/index.m3u8 |
| Working | Same | India TV | https://pl-indiatvnews.akamaized.net/out/v1/db79179b608641ceaa5a4d0dd0dca8da/index.m3u8 | https://pl-indiatvnews.akamaized.net/out/v1/db79179b608641ceaa5a4d0dd0dca8da/index.m3u8 |
| Working | Same | India TV Aap Ki Adalat (1080p) | https://amg01550-amg01550c6-samsung-in-4679.playouts.now.amagi.tv/playlist/amg01550-indiatvfast-indiatvakasamsung-samsungin/playlist.m3u8 | https://amg01550-amg01550c6-samsung-in-4679.playouts.now.amagi.tv/playlist/amg01550-indiatvfast-indiatvakasamsung-samsungin/playlist.m3u8 |
| Working | Same | India TV Speed News | https://cc-lyf4c0hwzg5dd.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-lyf4c0hwzg5dd/v1/vglive-sk-479089/main.m3u8 | https://cc-lyf4c0hwzg5dd.akamaized.net/v1/master/3722c60a815c199d9c0ef36c5b73da68a62b09d1/cc-lyf4c0hwzg5dd/v1/vglive-sk-479089/main.m3u8 |
| Working | Same | India Voice | https://d1msejlow1t3l4.cloudfront.net/fta/indiavoice/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/indiavoice/playlist.m3u8 |
| Working | Same | INH 24x7 | https://d1msejlow1t3l4.cloudfront.net/fta/inh24x7/playlist.m3u8 | https://d1msejlow1t3l4.cloudfront.net/fta/inh24x7/playlist.m3u8 |
| Working | Same | Janta TV | https://live.jswk.online/IK_RTPM/live/index.m3u8 | https://live.jswk.online/IK_RTPM/live/index.m3u8 |
| Working | Same | Jantantra TV | https://mumt05.tangotv.in/87NeALx2JANTANTRA/index.m3u8 | https://mumt05.tangotv.in/87NeALx2JANTANTRA/index.m3u8 |
| Non-working | Same | JK 24x7 News (720p) | https://live.gulistannews.in/hls/jk.m3u8 | https://live.gulistannews.in/hls/jk.m3u8 |
| Working | Same | K News India | https://legitpro.co.in/knews/index.m3u8 | https://legitpro.co.in/knews/index.m3u8 |
| Working | Same | Kadak | https://n18syndication.akamaized.net/bpk-tv/Kadak_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/Kadak_NW18_MOB/output01/master.m3u8 |
| Working | Same | Kashish News | https://server.thelegitpro.in/kashishnews/kashishnews/index.m3u8 | https://server.thelegitpro.in/kashishnews/kashishnews/index.m3u8 |
| Working | Same | KBC News | https://stream.ottlive.co.in/kbcnews/index.m3u8 | https://stream.ottlive.co.in/kbcnews/index.m3u8 |
| Working | Same | KBP Times | https://kbpnews.cloud/Kbptimes/Kbptimeslive/video.m3u8 | https://kbpnews.cloud/Kbptimes/Kbptimeslive/video.m3u8 |
| Working | Same | Khabar Fast | https://mumt04.tangotv.in/m18aqlK4KHABARFAST/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4KHABARFAST/index.m3u8 |
| Working | Same | Khabrain Abhi Tak | https://mumt05.tangotv.in/87NeALx2KHABRAINABHITAK/index.m3u8 | https://mumt05.tangotv.in/87NeALx2KHABRAINABHITAK/index.m3u8 |
| Working | Same | Live Times | https://stream.ottlive.co.in/livetimetv/index.m3u8 | https://stream.ottlive.co.in/livetimetv/index.m3u8 |
| Non-working | Same | Nagaland TV | https://mumt06.tangotv.in/qYyB8fXVNAGALANDTV/index.m3u8 | https://mumt06.tangotv.in/qYyB8fXVNAGALANDTV/index.m3u8 |
| Working | Same | Nation News | https://server.playontv.in/nationnews/index.m3u8 | https://server.playontv.in/nationnews/index.m3u8 |
| Working | Same | NDTV Good Times | https://amg01448-samsungin-ndtvgoodtimes-samsungin-ad-gp.amagi.tv/playlist/amg01448-samsungin-ndtvgoodtimes-samsungin/playlist.m3u8 | https://amg01448-samsungin-ndtvgoodtimes-samsungin-ad-gp.amagi.tv/playlist/amg01448-samsungin-ndtvgoodtimes-samsungin/playlist.m3u8 |
| Non-working | Same | NDTV India | http://103.213.31.109:90/StarUtsavMovies/playlist.m3u8 | http://103.213.31.109:90/StarUtsavMovies/playlist.m3u8 |
| Working | Same | NDTV Madhya Pradesh Chhattisgarh | https://ndtvregional.akamaized.net/hls/live/2102726-b/ndtvmpcg/master_1.m3u8 | https://ndtvregional.akamaized.net/hls/live/2102726-b/ndtvmpcg/master_1.m3u8 |
| Working | Same | NDTV Rajasthan | https://ndtvregional.akamaized.net/hls/live/2102726-b/ndtvraj/master_1.m3u8 | https://ndtvregional.akamaized.net/hls/live/2102726-b/ndtvraj/master_1.m3u8 |
| Working | Same | NE News | https://mumt05.tangotv.in/87NeALx2NENEWS/index.m3u8 | https://mumt05.tangotv.in/87NeALx2NENEWS/index.m3u8 |
| Working | Same | News 1 India | https://mumt07.tangotv.in/zHjX9OFlNEWS1INDIA/index.m3u8 | https://mumt07.tangotv.in/zHjX9OFlNEWS1INDIA/index.m3u8 |
| Working | Same | News 11 | https://mumt07.tangotv.in/zHjX9OFlNEWS11BHARAT/index.m3u8 | https://mumt07.tangotv.in/zHjX9OFlNEWS11BHARAT/index.m3u8 |
| Working | Same | News18 Bihar Jharkhand | https://n18syndication.akamaized.net/bpk-tv/News18_Bihar_Jharkhand_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_Bihar_Jharkhand_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Delhi NCR JK | https://n18syndication.akamaized.net/bpk-tv/News18_JKLH_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_JKLH_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 India | https://n18syndication.akamaized.net/bpk-tv/News18_India_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_India_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Madhya Pradesh/Chhattisgarh | https://n18syndication.akamaized.net/bpk-tv/News18_MP_Chhattisgarh_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_MP_Chhattisgarh_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Punjab/Haryana/Himachal | https://n18syndication.akamaized.net/bpk-tv/News18_Punjab_Haryana_HP_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_Punjab_Haryana_HP_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Rajasthan | https://n18syndication.akamaized.net/bpk-tv/News18_Rajasthan_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_Rajasthan_NW18_MOB/output01/master.m3u8 |
| Working | Same | News18 Uttar Pradesh Uttarakhand | https://n18syndication.akamaized.net/bpk-tv/News18_UP_Uttarakhand_NW18_MOB/output01/master.m3u8 | https://n18syndication.akamaized.net/bpk-tv/News18_UP_Uttarakhand_NW18_MOB/output01/master.m3u8 |
| Working | Same | News 24 | https://vidcdn.vidgyor.com/news24-origin/liveabr/playlist.m3u8 | https://vidcdn.vidgyor.com/news24-origin/liveabr/playlist.m3u8 |
| Working | Same | News 24 MP & Chhattisgarh | https://mumt04.tangotv.in/m18aqlK4NEWS24MPCG/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4NEWS24MPCG/index.m3u8 |
| Working | Same | News Daily 24 | https://mumt01.tangotv.in/O5aw8Zn3NEWSDAILY24/index.m3u8 | https://mumt01.tangotv.in/O5aw8Zn3NEWSDAILY24/index.m3u8 |
| Working | Same | News India 24x7 | https://cdn.pishow.tv/ott/live/273/master.m3u8 | https://cdn.pishow.tv/ott/live/273/master.m3u8 |
| Working | Same | News Nation | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/6cd2f649739a45ca9de1daf81cc7d0f2/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/6cd2f649739a45ca9de1daf81cc7d0f2/index.m3u8 |
| Working | Same | News Nation 81 | https://live.newsnation81.com/newsnation81/newsnation81/index.m3u8 | https://live.newsnation81.com/newsnation81/newsnation81/index.m3u8 |
| Working | Same | News State MP & CHG | https://jmp2.uk/stvp-IN4000012ML | https://jmp2.uk/stvp-IN4000012ML |
| Working | Same | News State Punjab Haryana Himachal | https://jmp2.uk/stvp-IN300083R1 | https://jmp2.uk/stvp-IN300083R1 |
| Working | Same | News State UP & UK | https://jmp2.uk/stvp-IN3000846P | https://jmp2.uk/stvp-IN3000846P |
| Working | Same | like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0" group-title="News",Northeast Live | https://server.thelegitpro.in/northeastlive/northeastlive/index.fmp4.m3u8 | https://server.thelegitpro.in/northeastlive/northeastlive/index.fmp4.m3u8 |
| Working | Same | NSC9 News | https://legitpro.co.in/nsc9/index.m3u8 | https://legitpro.co.in/nsc9/index.m3u8 |
| Working | Same | Only Bharat | https://mumt07.tangotv.in/zHjX9OFlONLYBHARAT/index.m3u8 | https://mumt07.tangotv.in/zHjX9OFlONLYBHARAT/index.m3u8 |
| Working | Same | Prime News | https://stream.ottlive.co.in/primenews/index.m3u8 | https://stream.ottlive.co.in/primenews/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="News",Public First | http://103.175.73.12:8080/live/237/master.m3u8 | http://103.175.73.12:8080/live/237/master.m3u8 |
| Non-working | Same | Raj Pariwar | http://103.72.101.252:8080/live/533.m3u8 | http://103.72.101.252:8080/live/533.m3u8 |
| Working | Same | Republic Bharat | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/RepublicBharat.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/RepublicBharat.m3u8 |
| Working | Same | Sach Bedhadak | https://sbnews.nexcdn.online/sbnews/live/index.m3u8 | https://sbnews.nexcdn.online/sbnews/live/index.m3u8 |
| Working | Same | Sadhna News Madhya Pradesh/Chhattisgarh | https://mumt04.tangotv.in/m18aqlK4SADHNEWSPMRAJ/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4SADHNEWSPMRAJ/index.m3u8 |
| Working | Same | Sadhna Plus News | https://6n3yow8pl9ok-hls-live.5centscdn.com/sadhananewstv/live.stream/playlist.m3u8 | https://6n3yow8pl9ok-hls-live.5centscdn.com/sadhananewstv/live.stream/playlist.m3u8 |
| Working | Same | Sahana News | https://mumt03.tangotv.in/Dsly5z3HSAHANANEWS/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HSAHANANEWS/index.m3u8 |
| Working | Same | Samachar Plus 24x7 | https://mumt05.tangotv.in/87NeALx2VERTENTSAMACHARPLUS/index.m3u8 | https://mumt05.tangotv.in/87NeALx2VERTENTSAMACHARPLUS/index.m3u8 |
| Working | Same | Sony BBC Earth HD | https://cloudplay-sonyliv.pages.dev/bbcearthhd.m3u8 | https://cloudplay-sonyliv.pages.dev/bbcearthhd.m3u8 |
| Working | Same | Sudarshan News | https://ott.livelegitpro.in/sudarshannews/sudarshannews/tracks-v1/index.fmp4.m3u8 | https://ott.livelegitpro.in/sudarshannews/sudarshannews/tracks-v1/index.fmp4.m3u8 |
| Working | Same | Swadesh News | https://cdn.pishow.tv/ott/live/465/master.m3u8 | https://cdn.pishow.tv/ott/live/465/master.m3u8 |
| Non-working | Same | Swaraj Express SMBC | https://mumt04.tangotv.in/m18aqlK4SWARAJEXPRESS/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4SWARAJEXPRESS/index.m3u8 |
| Working | Same | The Voice TV | https://legitpro.co.in/thevoicetv/thevoicetv/index.m3u8 | https://legitpro.co.in/thevoicetv/thevoicetv/index.m3u8 |
| Non-working | Same | Times Now (720p) | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/timesnow/timesnow_master.m3u8 | https://dztlhgid9me95.cloudfront.net/live-tv/Vidgyor/timesnow/timesnow_master.m3u8 |
| Working | Same | Times Now Navbharat | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/TimesNowNavbharat.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/TimesNowNavbharat.m3u8 |
| Non-working | Same | Times Now Navbharat HD | https://yupprestreamliveus.akamaized.net/v1/vglive-sk-717514/main.m3u8 | https://yupprestreamliveus.akamaized.net/v1/vglive-sk-717514/main.m3u8 |
| Working | Same | TNP News | https://server.thelegitpro.in/tnpnews/tnpnews/index.m3u8 | https://server.thelegitpro.in/tnpnews/tnpnews/index.m3u8 |
| Working | Same | TV9 Bharatvarsh | https://dyjmyiv3bp2ez.cloudfront.net/pub-iotv9hinjzgtpe/liveabr/playlist.m3u8 | https://dyjmyiv3bp2ez.cloudfront.net/pub-iotv9hinjzgtpe/liveabr/playlist.m3u8 |
| Working | Same | TV27 News | https://mumt04.tangotv.in/m18aqlK4TV27/index.m3u8 | https://mumt04.tangotv.in/m18aqlK4TV27/index.m3u8 |
| Working | Same | TV30 India | https://stream.tv30bharat.com/hls/shree/bhattji.m3u8 | https://stream.tv30bharat.com/hls/shree/bhattji.m3u8 |
| Working | Same | TV45 | https://server.livelegitpro.in/bnews24/bnews24/video.m3u8 | https://server.livelegitpro.in/bnews24/bnews24/video.m3u8 |
| Non-working | Same | VIP News | https://live.vipnews24x7.co.in/vipnews24x7/d0dbe915091d400bd8ee7f27f0791303.sdp/playlist.m3u8 | https://live.vipnews24x7.co.in/vipnews24x7/d0dbe915091d400bd8ee7f27f0791303.sdp/playlist.m3u8 |
| Working | Same | Vistaar News | https://stream.ottlive.co.in/vistaartv/index.m3u8 | https://stream.ottlive.co.in/vistaartv/index.m3u8 |
| Working | Same | Zee Bharat | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeehindustan/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/96bbab12-582e-4540-af70-510ab6824581/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeehindustan/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/96bbab12-582e-4540-af70-510ab6824581/main.m3u8 |
| Working | Same | Zee Delhi NCR Haryana | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeedelhincr/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/cc483a15-1b39-4642-872d-5d08d362ed01/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeedelhincr/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/cc483a15-1b39-4642-872d-5d08d362ed01/main.m3u8 |
| Working | Same | Zee Madhya Pradesh Chhattisgarh | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeemadhyachhattisgarh/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/2ab17056-6187-4f0e-a34d-f436ac479d6c/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeemadhyachhattisgarh/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/2ab17056-6187-4f0e-a34d-f436ac479d6c/main.m3u8 |
| Working | Same | Zee News | https://dknttpxmr0dwf.cloudfront.net/index_57.m3u8 | https://dknttpxmr0dwf.cloudfront.net/index_57.m3u8 |
| Working | Same | Zee Rajasthan | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeerajashthannews/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/8e864b9a-1681-41a0-99a6-387490bc5b24/main.m3u8 | https://vg-zeefta.akamaized.net/ptnr-yupptv/title-zeerajashthannews/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/8e864b9a-1681-41a0-99a6-387490bc5b24/main.m3u8 |
| Working | Same | Zee Uttar Pradesh/Uttarakhand | https://duw35ict5q7th.cloudfront.net/index_3.m3u8 | https://duw35ict5q7th.cloudfront.net/index_3.m3u8 |
| Working | Same | Zee Bihar Jharkhand | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/ZeeBiharJharkhand.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/ZeeBiharJharkhand.m3u8 |
| Working | Same | HMTV | https://cdn.pishow.tv/ott/live/280/master.m3u8 | https://cdn.pishow.tv/ott/live/280/master.m3u8 |
| Working | Same | India Today | https://d1rc86nwwc9fag.cloudfront.net/vglive-sk-293160/master.m3u8 | https://d1rc86nwwc9fag.cloudfront.net/vglive-sk-293160/master.m3u8 |
| Working | Same | Mirror Now | https://dai.google.com/linear/hls/event/ClPOullTQky5vGPf7fMZ8g/master.m3u8 | https://dai.google.com/linear/hls/event/ClPOullTQky5vGPf7fMZ8g/master.m3u8 |
| Working | Same | NDTV 24x7 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/NDTV24x7.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/NDTV24x7.m3u8 |
| Working | Same | NDTV Profit | https://ndtvprofit.akamaized.net/hls/live/2107404/ndtvprofit/chunklist_5.m3u8 | https://ndtvprofit.akamaized.net/hls/live/2107404/ndtvprofit/chunklist_5.m3u8 |
| Non-working | Same | NewsX | https://mumbai-edge.smartplaytv.in/NewsX/index.m3u8 | https://mumbai-edge.smartplaytv.in/NewsX/index.m3u8 |
| Working | Same | NewsX World | https://mumt03.tangotv.in/Dsly5z3HNEWSXWORLD/index.m3u8 | https://mumt03.tangotv.in/Dsly5z3HNEWSXWORLD/index.m3u8 |
| Working | Same | Republic TV | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/RepublicTV.m3u8 | https://raw.githubusercontent.com/amazeyourself/adaptive-streams/refs/heads/main/streams/in/YuppTV/RepublicTV.m3u8 |
| Non-working | Same | Times Now World | http://103.72.101.252:8080/live/876.m3u8 | http://103.72.101.252:8080/live/876.m3u8 |

## Science

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Non-working | Same | History TV18 HD | http://103.154.3.101:5001/live/577.m3u8 | http://103.154.3.101:5001/live/577.m3u8 |
| Working | Same | National Geographic (576p) | http://main.light-ott.net:80/play/live.php?mac=00:1A:79:17:28:41&stream=373017&extension=ts&play_token=zCaGy5dtla | http://main.light-ott.net:80/play/live.php?mac=00:1A:79:17:28:41&stream=373017&extension=ts&play_token=zCaGy5dtla |

## Sports

| Status | Match | Channel | Garden URL | 3502 URL |
|---|---|---|---|---|
| Working | Same | DD Sports | https://mumbai-edge.smartplaytv.in/DDSportsHD/index.m3u8 | https://mumbai-edge.smartplaytv.in/DDSportsHD/index.m3u8 |
| Working | Same | DD Sports SD | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/b17adfe543354fdd8d189b110617cddd/index.m3u8 | https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/b17adfe543354fdd8d189b110617cddd/index.m3u8 |
| Non-working | Same | Kabaddi 24x7 | http://180.188.254.253/live/KABADDI24X7.m3u8 | http://180.188.254.253/live/KABADDI24X7.m3u8 |
| Working | Same | Sony Sports Ten 3 Hindi | https://cloudplay-sonyliv.pages.dev/ten3.m3u8 | https://cloudplay-sonyliv.pages.dev/ten3.m3u8 |
| Working | Same | Sony Sports Ten 3 Hindi HD | https://cloudplay-sonyliv.pages.dev/ten3hd.m3u8 | https://cloudplay-sonyliv.pages.dev/ten3hd.m3u8 |
| Non-working | Same | Sports Squad Haryana | http://180.188.254.253/live/SPORTSSQUADHARYANA.m3u8 | http://180.188.254.253/live/SPORTSSQUADHARYANA.m3u8 |
| Non-working | Same | Star Sports 1 Hindi | http://103.253.18.58:8000/play/a03o | http://103.253.18.58:8000/play/a03o |
| Working | Same | Star Sports 2 HD | http://tvsen5.aynascope.net/cXPB2LKkErN9/index.m3u8 | http://tvsen5.aynascope.net/cXPB2LKkErN9/index.m3u8 |
| Working | Same | Star Sports 2 Hindi | https://tvsen5.aynaott.com/cXPB2LKkErN9/index.m3u8 | https://tvsen5.aynaott.com/cXPB2LKkErN9/index.m3u8 |
| Non-working | Same | Star Sports 2 Hindi HD | http://103.157.248.140:8000/play/a01m/index.m3u8 | http://103.157.248.140:8000/play/a01m/index.m3u8 |
| Non-working | Same | like Gecko) Chrome/147.0.0.0 Safari/537.36" group-title="Sports",Star Sports Khel | http://103.175.73.12:8080/live/151/151_0.m3u8 | http://103.175.73.12:8080/live/151/151_0.m3u8 |
| Working | Same | Star Sports Select 2 HD | http://tvsen7.aynascope.net/ssport2hd/index.m3u8 | http://tvsen7.aynascope.net/ssport2hd/index.m3u8 |
| Working | Same | like Gecko) Chrome/130.0.0.0 Safari/537.36" group-title="Sports",Unite8 Sports 2 | http://59.103.38.46:8000/play/a126/index.m3u8 | http://59.103.38.46:8000/play/a126/index.m3u8 |
| Non-working | Same | T Sports | https://tvsen5.aynaott.com/TnMn5kZz8aLm/index.m3u8 | https://tvsen5.aynaott.com/TnMn5kZz8aLm/index.m3u8 |
| Working | Same | Cricket Gold | https://streams2.sofast.tv/ptnr-yupptv/title-cricketgold/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/b2048bb8-1686-4432-aa50-647245383e0c/manifest.m3u8 | https://streams2.sofast.tv/ptnr-yupptv/title-cricketgold/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/b2048bb8-1686-4432-aa50-647245383e0c/manifest.m3u8 |
| Non-working | Same | ERT Sports 1 | http://hbbtvapp.ert.gr/stream.php/v/vid_ertsports_mpeg.2ts | http://hbbtvapp.ert.gr/stream.php/v/vid_ertsports_mpeg.2ts |
| Non-working | Same | ERT Sports 2 | http://hbbtvapp.ert.gr/stream.php/v/vid_ertplay2_mpeg.2ts | http://hbbtvapp.ert.gr/stream.php/v/vid_ertplay2_mpeg.2ts |
| Working | Same | Fox Sports 1 | http://85.237.89.160:9590/usa-s/FOX-SPORTS-1/index.m3u8 | http://85.237.89.160:9590/usa-s/FOX-SPORTS-1/index.m3u8 |
| Non-working | Same | Fox Sports 2 | https://tvsen7.aynascope.net/foxsports2/index.m3u8 | https://tvsen7.aynascope.net/foxsports2/index.m3u8 |
| Non-working | Same | PTV Sports | http://103.250.28.74:8000/play/a019/index.m3u8 | http://103.250.28.74:8000/play/a019/index.m3u8 |
| Non-working | Same | Sky Sports Cricket | https://leaf.highfly.dev/m3u/now-sky-sports-cricket/live.m3u8 | https://leaf.highfly.dev/m3u/now-sky-sports-cricket/live.m3u8 |
| Working | Same | Sky Sports Cricket HD | https://bl.rutube.ru/livestream/7c13a51576b9ff2601f08f5d57dd5169/index.m3u8?s=uiXES2ePt7xTpQnbJxn7Dg&e=2074684474&scheme=https | https://bl.rutube.ru/livestream/7c13a51576b9ff2601f08f5d57dd5169/index.m3u8?s=uiXES2ePt7xTpQnbJxn7Dg&e=2074684474&scheme=https |
| Working | Same | T Sports 7 | https://live-us1.thaimomo.com/live-as/chtsport-1/playlist.m3u8 | https://live-us1.thaimomo.com/live-as/chtsport-1/playlist.m3u8 |
| Non-working | Same | Willow | http://tvsen5.aynascope.net/willowhd/index.m3u8 | http://tvsen5.aynascope.net/willowhd/index.m3u8 |
| Working | Same | Willow Sports | https://d36r8jifhgsk5j.cloudfront.net/Willow_TV1080p.m3u8 | https://d36r8jifhgsk5j.cloudfront.net/Willow_TV1080p.m3u8 |
| Working | Same | Willow Sports | https://d36r8jifhgsk5j.cloudfront.net/Willow_TV.m3u8 | https://d36r8jifhgsk5j.cloudfront.net/Willow_TV.m3u8 |


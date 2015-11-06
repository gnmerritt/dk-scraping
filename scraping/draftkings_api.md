# Terms

`draft groups` - sets of players eligible to be picked with pricing information, start time, set of games

`contests` - individual games

`lineups` - a set of players from a draft group

# API endpoints (read)

## open contests:  https://www.draftkings.com/lobby/getcontests?sport=NFL

```javascript
"Contests": [
       {
           "a": 20.0,     // entry fee, in USD
           "attr": {
               "IsGuaranteed": "true",  // we need to only  submit teams to these
               "IsStarred": "true",
               "LobbyClass": "icon-d-crown"
           },
           "cs": 1,
           "cso": 0,
           "dg": 7462,   // draft group id, ties to scoring
           "dgpo": 21249156.0,
           "ec": 0,   // current # of entries associated w/ account
           "fpp": 80,
           "fwt": false,
           "id": 12080123,    // contest ID to submit to
           "isOwner": false,
           "m": 343500,     // max # of teams
           "mec": 500,      // multi-entry cap, max # of entries per account?
           "n": "NFL $6M Millionaire Maker [$1M to 1st]",
           "nt": 206297,     // current # of teams
           "pd": {
               "Cash": "6000000"  // amount of guaranteed cash, USD
           },
           "po": 6000000,
           "pt": 1,
           "rl": false,
           "rlc": 0,
           "rll": 99999,
           "s": 1,
           "sa": true,
           "sd": "/Date(1445792400000)/", // start date, UTC?
           "sdstring": "Sun 1:00PM",
           "so": -99999999,
           "ssd": null,
           "startTimeType": 0,
           "tix": false,
           "tmpl": 244309,
           "uc": 0,
           "ulc": 0
       },
       {
           // tons more contests here
       }
   ]
 "DraftGroups": [
        {
            "ContestStartTimeSuffix": " (Primetime)",
            "ContestStartTimeType": 0,
            "ContestTypeId": 21,
            "DraftGroupId": 7508,  // pointer to the player pricing information for this contest
            "GameCount": 2,        // # of NFL games
            "Games": null,
            "Sport": "NFL",
            "StartDate": "2015-10-26T00:30:00.0000000Z",    // UTC
            "StartDateEst": "2015-10-25T20:30:00.0000000"   // EST
        },
        {
            // looks like 2-3 of these running at a theaigame
            // e.g. Sunday, Monday, Th-Sunday
        }
    ]
```

## players for a contest: https://www.draftkings.com/lineup/getavailableplayers?draftGroupId=7462

```javascript
{
"ExceptionalMessages": [],
"IsDisabledFromDrafting": false,
"atabbr": "Atl", // away team abbrv
"atid": 323,     // away team id
"fn": "Julio",   // first name
"fnu": "Julio",
"htabbr": "Ten",   // home team abbrv.
"htid": 336,       // home team id
"i": "",
"ln": "Jones",    // last name
"lnu": "Jones",
"news": 1,
"or": 7,
"pcode": 24793,
"pid": 456614,    // player id, used in lineups
"pn": "WR",       // fantasy position
"posid": 3,
"pp": 0,        // current score?
"ppg": "25.3",   // PPG projection
"s": 9100,      // salary": $9,100
"slo": null,
"swp": true,
"tid": 323,   // player's team id
"tsid": 3149029,
}
```

# API endpoints (submit a lineup, enter a contest)

## `POST` https://www.draftkings.com/contest/joincontestflow

not sure what this does yet. in the browser it shows a confirmation window

## `POST` https://www.draftkings.com/contest/joincontest

Request-Body:
```javascript
hiddenRoster:[
    {"id":184503,"ts":3149772,"rpid":66},
    {"id":335112,"ts":3149139,"rpid":67},
    {"id":467405,"ts":3149144,"rpid":67},
    {"id":468655,"ts":3149122,"rpid":68},
    {"id":650914,"ts":3149144,"rpid":68},
    {"id":589991,"ts":3149073,"rpid":68},
    {"id":234249,"ts":3149144,"rpid":69},
    {"id":164505,"ts":3149768,"rpid":70},
    {"id":323,"ts":3149029,"rpid":71}
]
```
and
```
Edit:False
UserContestId:0
hidden_contest:12181244
joinContests:12181244
response_error:
```

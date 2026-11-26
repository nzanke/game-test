// 特別教室棟4階の廊下（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）
G.defineMap('annex4f', {
 "name": "特別教室棟4階",
 "tiles": [
  "#411111714171417141714444#",
  "#522222825282528252825555#",
  "#633333936393639363936666#",
  "#,,,,,,,,,,,,,,,,,,,,,^^,#",
  "#,,,,,,,,,,,,,,,,,,,,,^^,#",
  "#,,,,,,,,,,,,,,,,,,,,,,,,#",
  "#,,,,,,,,,,,,,,,,,,,,,,,,#",
  "##########################"
 ],
 "signs": [
  {
   "x": 7,
   "y": 0,
   "text": "音楽室"
  },
  {
   "x": 11,
   "y": 0,
   "text": "音楽準備室"
  },
  {
   "x": 15,
   "y": 0,
   "text": "資料室"
  },
  {
   "x": 19,
   "y": 0,
   "text": "資料室２"
  },
  {
   "x": 22,
   "y": 0,
   "text": "階段"
  }
 ],
 "events": [
  {
   "id": "door7",
   "x": 7,
   "y": 2,
   "pages": [
    {
     "trigger": "touch",
     "priority": "same",
     "sensor": false,
     "list": [
      [
       "se",
       "door"
      ],
      [
       "enter",
       "room_music",
       8,
       3,
       "down",
       "音楽室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door11",
   "x": 11,
   "y": 2,
   "pages": [
    {
     "trigger": "touch",
     "priority": "same",
     "sensor": false,
     "list": [
      [
       "se",
       "buzzer"
      ],
      [
       "text",
       "",
       "音楽準備室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door15",
   "x": 15,
   "y": 2,
   "pages": [
    {
     "trigger": "touch",
     "priority": "same",
     "sensor": false,
     "list": [
      [
       "se",
       "buzzer"
      ],
      [
       "text",
       "",
       "資料室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door19",
   "x": 19,
   "y": 2,
   "pages": [
    {
     "trigger": "touch",
     "priority": "same",
     "sensor": false,
     "list": [
      [
       "se",
       "buzzer"
      ],
      [
       "text",
       "",
       "資料室２には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsE0",
   "x": 22,
   "y": 3,
   "pages": [
    {
     "trigger": "touch",
     "priority": "below",
     "sensor": false,
     "list": [
      [
       "choice",
       [
        "3階へ下りる",
        "やめる"
       ],
       [
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "annex3f",
          52,
          5,
          "down"
         ]
        ],
        []
       ],
       {
        "cancel": 1
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsE1",
   "x": 23,
   "y": 3,
   "pages": [
    {
     "trigger": "touch",
     "priority": "below",
     "sensor": false,
     "list": [
      [
       "choice",
       [
        "3階へ下りる",
        "やめる"
       ],
       [
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "annex3f",
          52,
          5,
          "down"
         ]
        ],
        []
       ],
       {
        "cancel": 1
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsE2",
   "x": 22,
   "y": 4,
   "pages": [
    {
     "trigger": "touch",
     "priority": "below",
     "sensor": false,
     "list": [
      [
       "choice",
       [
        "3階へ下りる",
        "やめる"
       ],
       [
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "annex3f",
          52,
          5,
          "down"
         ]
        ],
        []
       ],
       {
        "cancel": 1
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsE3",
   "x": 23,
   "y": 4,
   "pages": [
    {
     "trigger": "touch",
     "priority": "below",
     "sensor": false,
     "list": [
      [
       "choice",
       [
        "3階へ下りる",
        "やめる"
       ],
       [
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "annex3f",
          52,
          5,
          "down"
         ]
        ],
        []
       ],
       {
        "cancel": 1
       }
      ]
     ]
    }
   ]
  }
 ]
});

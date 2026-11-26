// 本館1階の廊下（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）
G.defineMap('main1f', {
 "name": "本館1階",
 "tiles": [
  "#444441111171417141117141714171417144444111117141111171417141714444411171411171#",
  "#555552222282528252228252825282528255555222228252222282528252825555522282522282#",
  "#666663333393639363339363936393639366666333339363333393639363936666633393633393#",
  "#.^^................................^^..........................^^.............#",
  "#.^^................................^^..........................^^.............#",
  "#..............................................................................#",
  "#..............................................................................#",
  "################################################################################"
 ],
 "signs": [
  {
   "x": 2,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 11,
   "y": 0,
   "text": "昇降口"
  },
  {
   "x": 15,
   "y": 0,
   "text": "用務員室"
  },
  {
   "x": 21,
   "y": 0,
   "text": "玄関"
  },
  {
   "x": 25,
   "y": 0,
   "text": "事務室"
  },
  {
   "x": 29,
   "y": 0,
   "text": "校長室"
  },
  {
   "x": 33,
   "y": 0,
   "text": "応接室"
  },
  {
   "x": 36,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 45,
   "y": 0,
   "text": "会議室"
  },
  {
   "x": 53,
   "y": 0,
   "text": "進路室"
  },
  {
   "x": 57,
   "y": 0,
   "text": "渡り廊下"
  },
  {
   "x": 61,
   "y": 0,
   "text": "トイレ"
  },
  {
   "x": 64,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 71,
   "y": 0,
   "text": "談話室"
  },
  {
   "x": 77,
   "y": 0,
   "text": "保健室"
  }
 ],
 "events": [
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
       "text",
       "",
       "外へ出るのは、また今度にしよう。"
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
       "用務員室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door21",
   "x": 21,
   "y": 2,
   "pages": [
    {
     "trigger": "touch",
     "priority": "same",
     "sensor": false,
     "list": [
      [
       "text",
       "",
       "外へ出るのは、また今度にしよう。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door25",
   "x": 25,
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
       "事務室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door29",
   "x": 29,
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
       "校長室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door33",
   "x": 33,
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
       "応接室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door45",
   "x": 45,
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
       "room_lecture",
       8,
       3,
       "down",
       "会議室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door53",
   "x": 53,
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
       "room_office",
       8,
       3,
       "down",
       "進路室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door57",
   "x": 57,
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
       "transfer",
       "annex1f",
       43,
       3,
       "down"
      ]
     ]
    }
   ]
  },
  {
   "id": "door61",
   "x": 61,
   "y": 2,
   "pages": [
    {
     "trigger": "touch",
     "priority": "same",
     "sensor": false,
     "list": [
      [
       "text",
       "",
       "トイレだ。いまは用はない。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door71",
   "x": 71,
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
       "room_lecture",
       8,
       3,
       "down",
       "談話室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door77",
   "x": 77,
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
       "room1",
       12,
       3,
       "down",
       "保健室"
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsW0",
   "x": 2,
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
        "2階へ上る",
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
          "main2f",
          2,
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
   "id": "stairsW1",
   "x": 3,
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
        "2階へ上る",
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
          "main2f",
          2,
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
   "id": "stairsW2",
   "x": 2,
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
        "2階へ上る",
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
          "main2f",
          2,
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
   "id": "stairsW3",
   "x": 3,
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
        "2階へ上る",
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
          "main2f",
          2,
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
   "id": "stairsM0",
   "x": 36,
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
        "2階へ上る",
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
          "main2f",
          44,
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
   "id": "stairsM1",
   "x": 37,
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
        "2階へ上る",
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
          "main2f",
          44,
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
   "id": "stairsM2",
   "x": 36,
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
        "2階へ上る",
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
          "main2f",
          44,
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
   "id": "stairsM3",
   "x": 37,
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
        "2階へ上る",
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
          "main2f",
          44,
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
   "id": "stairsE0",
   "x": 64,
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
        "2階へ上る",
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
          "main2f",
          68,
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
   "x": 65,
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
        "2階へ上る",
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
          "main2f",
          68,
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
   "x": 64,
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
        "2階へ上る",
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
          "main2f",
          68,
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
   "x": 65,
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
        "2階へ上る",
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
          "main2f",
          68,
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

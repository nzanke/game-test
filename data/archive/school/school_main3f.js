// 本館3階の廊下（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）
G.defineMap('main3f', {
 "name": "本館3階",
 "tiles": [
  "#44444111117141111171411111714111117141111171411111714444411171411111714171417144444111117141111171#",
  "#55555222228252222282522222825222228252222282522222825555522282522222825282528255555222228252222282#",
  "#66666333339363333393633333936333339363333393633333936666633393633333936393639366666333339363333393#",
  "#.^^..................................................^^........................^^.................#",
  "#.^^..................................................^^........................^^.................#",
  "#..................................................................................................#",
  "#..................................................................................................#",
  "####################################################################################################"
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
   "text": "2の3"
  },
  {
   "x": 19,
   "y": 0,
   "text": "2の4"
  },
  {
   "x": 27,
   "y": 0,
   "text": "2の5"
  },
  {
   "x": 35,
   "y": 0,
   "text": "第二進路室"
  },
  {
   "x": 43,
   "y": 0,
   "text": "2の6"
  },
  {
   "x": 51,
   "y": 0,
   "text": "2の7"
  },
  {
   "x": 54,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 61,
   "y": 0,
   "text": "自習室"
  },
  {
   "x": 69,
   "y": 0,
   "text": "3の1"
  },
  {
   "x": 73,
   "y": 0,
   "text": "国語資料室"
  },
  {
   "x": 77,
   "y": 0,
   "text": "トイレ"
  },
  {
   "x": 80,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 89,
   "y": 0,
   "text": "3の2"
  },
  {
   "x": 97,
   "y": 0,
   "text": "3の3"
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
       "se",
       "door"
      ],
      [
       "enter",
       "classroom",
       14,
       3,
       "down",
       "2の3"
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
       "door"
      ],
      [
       "enter",
       "classroom",
       14,
       3,
       "down",
       "2の4"
      ]
     ]
    }
   ]
  },
  {
   "id": "door27",
   "x": 27,
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
       "classroom",
       14,
       3,
       "down",
       "2の5"
      ]
     ]
    }
   ]
  },
  {
   "id": "door35",
   "x": 35,
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
       "第二進路室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door43",
   "x": 43,
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
       "classroom",
       14,
       3,
       "down",
       "2の6"
      ]
     ]
    }
   ]
  },
  {
   "id": "door51",
   "x": 51,
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
       "classroom",
       14,
       3,
       "down",
       "2の7"
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
       "se",
       "door"
      ],
      [
       "enter",
       "room_lecture",
       8,
       3,
       "down",
       "自習室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door69",
   "x": 69,
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
       "classroom",
       14,
       3,
       "down",
       "3の1"
      ]
     ]
    }
   ]
  },
  {
   "id": "door73",
   "x": 73,
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
       "国語資料室には鍵がかかっている。"
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
       "text",
       "",
       "トイレだ。いまは用はない。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door89",
   "x": 89,
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
       "classroom",
       14,
       3,
       "down",
       "3の2"
      ]
     ]
    }
   ]
  },
  {
   "id": "door97",
   "x": 97,
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
       "classroom",
       14,
       3,
       "down",
       "3の3"
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          2,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          2,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          2,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          2,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsM0",
   "x": 54,
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          52,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsM1",
   "x": 55,
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          52,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsM2",
   "x": 54,
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          52,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsM3",
   "x": 55,
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          52,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsE0",
   "x": 80,
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          80,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsE1",
   "x": 81,
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          80,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsE2",
   "x": 80,
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          80,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  },
  {
   "id": "stairsE3",
   "x": 81,
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
        "4階へ上る",
        "2階へ下りる",
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
          "main4f",
          80,
          5,
          "down"
         ]
        ],
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
        "cancel": 2
       }
      ]
     ]
    }
   ]
  }
 ]
});

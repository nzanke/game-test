// 本館4階の廊下（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）
G.defineMap('main4f', {
 "name": "本館4階",
 "tiles": [
  "#44444111117141111171411111714111714111117141111171444441111171411111714171417144444111117141111171#",
  "#55555222228252222282522222825222825222228252222282555552222282522222825282528255555222228252222282#",
  "#66666333339363333393633333936333936333339363333393666663333393633333936393639366666333339363333393#",
  "#.^^................................................^^..........................^^.................#",
  "#.^^................................................^^..........................^^.................#",
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
   "text": "2の2"
  },
  {
   "x": 19,
   "y": 0,
   "text": "2の1"
  },
  {
   "x": 27,
   "y": 0,
   "text": "1の7"
  },
  {
   "x": 33,
   "y": 0,
   "text": "生徒会室"
  },
  {
   "x": 41,
   "y": 0,
   "text": "1の6"
  },
  {
   "x": 49,
   "y": 0,
   "text": "1の5"
  },
  {
   "x": 52,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 61,
   "y": 0,
   "text": "1の4"
  },
  {
   "x": 69,
   "y": 0,
   "text": "1の3"
  },
  {
   "x": 73,
   "y": 0,
   "text": "教科資料室"
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
   "text": "1の2"
  },
  {
   "x": 97,
   "y": 0,
   "text": "1の1"
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
       "2の2"
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
       "2の1"
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
       "1の7"
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
       "door"
      ],
      [
       "enter",
       "room_lecture",
       8,
       3,
       "down",
       "生徒会室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door41",
   "x": 41,
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
       "1の6"
      ]
     ]
    }
   ]
  },
  {
   "id": "door49",
   "x": 49,
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
       "1の5"
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
       "classroom",
       14,
       3,
       "down",
       "1の4"
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
       "1の3"
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
       "教科資料室には鍵がかかっている。"
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
       "1の2"
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
       "1の1"
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
          "main3f",
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
          "main3f",
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
          "main3f",
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
          "main3f",
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
   "x": 52,
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
          "main3f",
          54,
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
   "x": 53,
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
          "main3f",
          54,
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
   "x": 52,
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
          "main3f",
          54,
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
   "x": 53,
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
          "main3f",
          54,
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
          "main3f",
          80,
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
          "main3f",
          80,
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
          "main3f",
          80,
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
          "main3f",
          80,
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

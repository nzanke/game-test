// 本館2階の廊下（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）
G.defineMap('main2f', {
 "name": "本館2階",
 "tiles": [
  "#44444111111111714171417141714111117141117144444111117141111171417144444111117141111171#",
  "#55555222222222825282528252825222228252228255555222228252222282528255555222228252222282#",
  "#66666333333333936393639363936333339363339366666333339363333393639366666333339363333393#",
  "#.^^........................................^^......................^^.................#",
  "#.^^........................................^^......................^^.................#",
  "#......................................................................................#",
  "#......................................................................................#",
  "########################################################################################"
 ],
 "signs": [
  {
   "x": 2,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 15,
   "y": 0,
   "text": "職員室"
  },
  {
   "x": 19,
   "y": 0,
   "text": "ロッカー"
  },
  {
   "x": 23,
   "y": 0,
   "text": "印刷室"
  },
  {
   "x": 27,
   "y": 0,
   "text": "放送室"
  },
  {
   "x": 35,
   "y": 0,
   "text": "学習指導室"
  },
  {
   "x": 41,
   "y": 0,
   "text": "多目的室"
  },
  {
   "x": 44,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 53,
   "y": 0,
   "text": "3の7"
  },
  {
   "x": 61,
   "y": 0,
   "text": "3の6"
  },
  {
   "x": 65,
   "y": 0,
   "text": "トイレ"
  },
  {
   "x": 68,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 77,
   "y": 0,
   "text": "3の5"
  },
  {
   "x": 85,
   "y": 0,
   "text": "3の4"
  }
 ],
 "events": [
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
       "door"
      ],
      [
       "enter",
       "room_office",
       8,
       3,
       "down",
       "職員室"
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
       "ロッカーには鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door23",
   "x": 23,
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
       "印刷室には鍵がかかっている。"
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
       "buzzer"
      ],
      [
       "text",
       "",
       "放送室には鍵がかかっている。"
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
       "学習指導室"
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
       "room_lecture",
       8,
       3,
       "down",
       "多目的室"
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
       "classroom",
       14,
       3,
       "down",
       "3の7"
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
       "3の6"
      ]
     ]
    }
   ]
  },
  {
   "id": "door65",
   "x": 65,
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
       "classroom",
       14,
       3,
       "down",
       "3の5"
      ]
     ]
    }
   ]
  },
  {
   "id": "door85",
   "x": 85,
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
       "3の4"
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
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
   "x": 44,
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
          36,
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
   "x": 45,
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
          36,
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
   "x": 44,
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
          36,
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
   "x": 45,
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
          36,
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
   "x": 68,
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
          64,
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
   "x": 69,
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
          64,
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
   "x": 68,
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
          64,
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
   "x": 69,
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
        "3階へ上る",
        "1階へ下りる",
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
        [
         [
          "se",
          "door"
         ],
         [
          "transfer",
          "main1f",
          64,
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

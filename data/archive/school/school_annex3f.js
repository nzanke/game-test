// 特別教室棟3階の廊下（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）
G.defineMap('annex3f', {
 "name": "特別教室棟3階",
 "tiles": [
  "#444441111111714171417141117141111171417141117141714444411171#",
  "#555552222222825282528252228252222282528252228252825555522282#",
  "#666663333333936393639363339363333393639363339363936666633393#",
  "#,^^,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,^^,,,,,,,#",
  "#,^^,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,^^,,,,,,,#",
  "#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,#",
  "#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,#",
  "##############################################################"
 ],
 "signs": [
  {
   "x": 2,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 13,
   "y": 0,
   "text": "図書室"
  },
  {
   "x": 17,
   "y": 0,
   "text": "作業室"
  },
  {
   "x": 21,
   "y": 0,
   "text": "書庫"
  },
  {
   "x": 27,
   "y": 0,
   "text": "学習室"
  },
  {
   "x": 35,
   "y": 0,
   "text": "パソコン室"
  },
  {
   "x": 39,
   "y": 0,
   "text": "映写室"
  },
  {
   "x": 45,
   "y": 0,
   "text": "視聴覚室"
  },
  {
   "x": 49,
   "y": 0,
   "text": "LL準備室"
  },
  {
   "x": 52,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 59,
   "y": 0,
   "text": "スタディルーム"
  }
 ],
 "events": [
  {
   "id": "door17",
   "x": 17,
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
       "作業室には鍵がかかっている。"
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
       "se",
       "buzzer"
      ],
      [
       "text",
       "",
       "書庫には鍵がかかっている。"
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
       "room_lecture",
       8,
       3,
       "down",
       "学習室"
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
       "room_pc",
       8,
       3,
       "down",
       "パソコン室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door39",
   "x": 39,
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
       "映写室には鍵がかかっている。"
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
       "視聴覚室"
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
       "buzzer"
      ],
      [
       "text",
       "",
       "LL準備室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door59",
   "x": 59,
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
       "スタディルーム"
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
          "annex2f",
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
          "annex2f",
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
          "annex2f",
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
          "annex2f",
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
   "id": "stairsE0",
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
          "annex4f",
          22,
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
          "annex2f",
          50,
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
          "annex4f",
          22,
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
          "annex2f",
          50,
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
          "annex4f",
          22,
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
          "annex2f",
          50,
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
          "annex4f",
          22,
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
          "annex2f",
          50,
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

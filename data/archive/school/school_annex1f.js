// 特別教室棟1階の廊下（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）
G.defineMap('annex1f', {
 "name": "特別教室棟1階",
 "tiles": [
  "#4444411111714171417141117141117141111171417141714171444441111171#",
  "#5555522222825282528252228252228252222282528252825282555552222282#",
  "#6666633333936393639363339363339363333393639363936393666663333393#",
  "#,^^,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,^^,,,,,,,,,#",
  "#,^^,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,^^,,,,,,,,,#",
  "#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,#",
  "#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,#",
  "##################################################################"
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
   "text": "調理室"
  },
  {
   "x": 15,
   "y": 0,
   "text": "調理準備室"
  },
  {
   "x": 19,
   "y": 0,
   "text": "被服準備室"
  },
  {
   "x": 25,
   "y": 0,
   "text": "被服室"
  },
  {
   "x": 31,
   "y": 0,
   "text": "生化講義室"
  },
  {
   "x": 39,
   "y": 0,
   "text": "化学実験室"
  },
  {
   "x": 43,
   "y": 0,
   "text": "渡り廊下（特別教室棟）"
  },
  {
   "x": 47,
   "y": 0,
   "text": "化学準備室"
  },
  {
   "x": 51,
   "y": 0,
   "text": "生物準備室"
  },
  {
   "x": 54,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 63,
   "y": 0,
   "text": "生物実験室"
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
       "room_lab",
       8,
       3,
       "down",
       "調理室"
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
       "調理準備室には鍵がかかっている。"
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
       "被服準備室には鍵がかかっている。"
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
       "door"
      ],
      [
       "enter",
       "room_lecture",
       8,
       3,
       "down",
       "被服室"
      ]
     ]
    }
   ]
  },
  {
   "id": "door31",
   "x": 31,
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
       "生化講義室"
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
       "door"
      ],
      [
       "enter",
       "room_lab",
       8,
       3,
       "down",
       "化学実験室"
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
       "transfer",
       "main1f",
       57,
       3,
       "down"
      ]
     ]
    }
   ]
  },
  {
   "id": "door47",
   "x": 47,
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
       "化学準備室には鍵がかかっている。"
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
       "buzzer"
      ],
      [
       "text",
       "",
       "生物準備室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door63",
   "x": 63,
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
       "room_lab",
       8,
       3,
       "down",
       "生物実験室"
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
          "annex2f",
          50,
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
          "annex2f",
          50,
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
          "annex2f",
          50,
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
          "annex2f",
          50,
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

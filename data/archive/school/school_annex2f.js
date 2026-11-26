// 特別教室棟2階の廊下（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）
G.defineMap('annex2f', {
 "name": "特別教室棟2階",
 "tiles": [
  "#4444411111714171417141117141117141111171417141714444417141111171#",
  "#5555522222825282528252228252228252222282528252825555528252222282#",
  "#6666633333936393639363339363339363333393639363936666639363333393#",
  "#,^^,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,^^,,,,,,,,,,,,,#",
  "#,^^,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,^^,,,,,,,,,,,,,#",
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
   "text": "美術室"
  },
  {
   "x": 15,
   "y": 0,
   "text": "美術準備室"
  },
  {
   "x": 19,
   "y": 0,
   "text": "社会科準備室"
  },
  {
   "x": 25,
   "y": 0,
   "text": "社会科教室"
  },
  {
   "x": 31,
   "y": 0,
   "text": "物地講義室"
  },
  {
   "x": 39,
   "y": 0,
   "text": "物理実験室"
  },
  {
   "x": 43,
   "y": 0,
   "text": "物理準備室"
  },
  {
   "x": 47,
   "y": 0,
   "text": "暗室"
  },
  {
   "x": 50,
   "y": 0,
   "text": "階段"
  },
  {
   "x": 55,
   "y": 0,
   "text": "地学準備室"
  },
  {
   "x": 63,
   "y": 0,
   "text": "地学実験室"
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
       "room_art",
       8,
       3,
       "down",
       "美術室"
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
       "美術準備室には鍵がかかっている。"
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
       "社会科準備室には鍵がかかっている。"
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
       "社会科教室"
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
       "物地講義室"
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
       "物理実験室"
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
       "buzzer"
      ],
      [
       "text",
       "",
       "物理準備室には鍵がかかっている。"
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
       "暗室には鍵がかかっている。"
      ]
     ]
    }
   ]
  },
  {
   "id": "door55",
   "x": 55,
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
       "地学準備室には鍵がかかっている。"
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
       "地学実験室"
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
          "annex3f",
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
          "annex1f",
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
          "annex3f",
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
          "annex1f",
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
          "annex3f",
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
          "annex1f",
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
          "annex3f",
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
          "annex1f",
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
   "id": "stairsE0",
   "x": 50,
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
          "annex3f",
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
          "annex1f",
          54,
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
   "x": 51,
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
          "annex3f",
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
          "annex1f",
          54,
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
   "x": 50,
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
          "annex3f",
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
          "annex1f",
          54,
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
   "x": 51,
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
          "annex3f",
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
          "annex1f",
          54,
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

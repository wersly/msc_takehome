class Config(object):

    DB_FILE = "orchestra.db"
    REPORTS = [
        {
            "view": "all_musicians",
            "name": "Name, instrument, and section for all musicians"
        },
        {
            "view": "instruments_without_musicians",
            "name": "Instruments that don't yet have musicians (i.e. no one plays the trumpet), and their sections"
        },
        {
            "view": "multi_instrumentalists",
            "name": "Any musicians that play two or more instruments, their instrument, and section"
        },
        {
            "view": "multiple_players",
            "name": "Any instruments that are played by multiple musicians, as well as the musician names and sections"
        }
    ]

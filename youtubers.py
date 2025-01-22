class Youtuber:
    def __init__(self, name, group_id, pl_id):
        self.name = name #имя ютубера после @
        self.group_id = group_id 
        self.pl_id = pl_id #номер плейлиста в группе вк

youtubers_list = [
    Youtuber(name, group_id, pl_id),   #короткая ссылка на ютубера в поле name, айди группы в вк в поле group_id, айди плейлиста в поле pl_id
    Youtuber(name, group_id, pl_id),
    Youtuber(name, group_id, pl_id),
    Youtuber(name, group_id, pl_id),
    Youtuber(name, group_id, pl_id),
    Youtuber(name, group_id, pl_id)
    # и так далее
]

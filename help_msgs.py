admin_msg = {

1:
'"написать сергей беспалов анон\n\
завтра бухаем\n\
и это не обсуждается"\n\
— (lvl 1) отправляет челу с указанным именем и фамилией сообщение, которое ты написал, можно много строчное, если указать после имени анон, то твое имя ему не сообщат',

6:
'"позвать бухать Женя Калинин"\n\
— (lvl 6) указанный чел автоматически позван бухать (анонимно)',

7:
'"послать 282727267"\n\
— (lvl 7) челу с указанным вк id приходит обидная анонимка (либо вместо айди можно имя фамилию из вк)',

10:
'"редактировать пн\n\
новое расписание на понедельник"\n\
— (admin 10) заменить расписание в указанный день',

30:
'"creategroup 381904"\n\
— (admin 30) создает группу с номером 381904',

100:
'"setadmin 284628937 999"\n\
— (admin 100) устанавливает челу с указанным вкайди доступ уровня 999 (нельзя менять уровень админки перманентно забаненным, нельзя ставить лвл выше своего, снижать урвоень можно только со 101 уровня\n\
"ban 624030526 17"\n\
— (admin 100) бан нахуй (на 17 часов)',

101:
'"unban 624030526"\n\
— (admin 101) разбан чела с указанным айди',

300:
'"permoban 624030526"\n\
— (admin 300) перманентный бан чела без возможности разбана вообще',

500:
'"update db"\n\
— (admin 500) обновляет базу данных, которая хранится в постоянной памяти\n\
"restore db"\n\
— (admin 500) подгружает базу данных, которая хранится в постоянной памяти взамен той что уже есть в озу\n\
"стоп"\n\
— (admin 500) вырубить нахуй бота\nче ты с ним разговариваешь, въеби ему'

}

nonadmin_msg = 'Типа список команд бота:\n\
(регистр не имеет значения, можете писать хоть капсом, хоть маленькими)\n\
\n\
1. Расписание пар (пока только 381904)\n\
"пн" или "понедельник" или любой др. день недели \n\
— расписание на этот день для недели, которая идет сейчас (так что если хочешь посмотреть некст неделю, юзай полное "расписание" или "завтра")\n\
"сегодня", "завтра"\n\
— расписание на соответствующий день с учетом четности недели (если задавалось)\n\
"расписание"\n\
— выкидывает расписание на всю неделю одним сооьщением\n\
"неделя"\n\
— четность текущей недели\n\
"группа 381904"\n\
— запоминает что ты из группы 381904\n\
\n\
2. Общение с другими пользователями  (период между выполнением 2 мин)\n\
"поздравить данила"\n\
— Данилу Пулю приходит поздравление с др от твоего имени\n\
"список людей"\n\
— список пользователей\n\
"топ людей"\n\
— актуальные топа пользователей\n\
другие по правам доступа 1-9\n\
\n\
3. Другие функции\n\
"мои данные"\n\
— отображает твои данные, которые сохранены у бота\n\
"заспамить админа\n\
бот хуй#я"\n\
— сообщить админу о критической неисправности бота\n\
"переведи\n\
ghbdtn отл_пфьуы\n\
— вернет тебе привет jnk_games (типа исправляет раскладку окда)\nа вообще можешь пересылать боту чьито сообщения, которые нао исправить и написать переведи\n\
"поиск python language"\n\
— ищет в поисковике duckduckgo вас запрос и отправляет короткий ответ, типа самый релевантный, если он есть, тольько запросы на енглише((\n\
"джони"\n\
— wake the fuck up the samourai\n\
"сменить ник ПАТАУ_peek"\n\
— меняет ваш ник на указанный (по умолчанию ник это имя (только 1 слово)), чтобы можно было писать сообщ по этому нику и мб потом еще чтонибудь\n\
"шутка" или "анекдот" или "разрывная"\n\
— бот напишет анекдот\n\
"гачи топ"\n\
— бот отправит рандомный трек из топ 20 гачи ремиксов по версии jnk gms\n\
"help" или "команды"\n\
— отобразить это сооьщение\n\
"буст сооьщений"\n\
— топ сикрет чит команда для накрутки числа сообщений для акции\n\
\n\
4. Если хочется поговорить с ботом (чел тебе поговорить нескем больше?🤨)\n\
список слов, на которые реагирует бот:\n\
"кто ты"\n\
"привет" и подобные\n\
"да", "нет", "але", "ладно", "спасибо" и другие, а еще куча матов)0)\n'


def constructHelpMsg(admin_lvl):
    msg = nonadmin_msg
    if admin_lvl > 0:
        msg += '\n\nкоманды, доступные на твоем уровне админки:\n\n'
    for lvl in admin_msg:
        if lvl > admin_lvl:
            break
        msg += admin_msg[lvl] + '\n'
    return msg

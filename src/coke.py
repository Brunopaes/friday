# -*- coding: utf-8 -*-
import helpers
import random


def insert_coke(message):
    """Function to add ingested coke.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg : success or failure message - to be displayed at Telegram's chat.

    """
    message_text = message.text.lower().split(' ')
    try:
        value = float(message_text[-1])
    except ValueError:
        return 'Cannot add non-numeric values!'

    helpers.set_path()
    client = helpers.start_connection()

    user_id = message.from_user.id
    username = '{} {}'.format(
        message.from_user.first_name,
        message.from_user.last_name
    )

    client.query("""
    INSERT INTO
        `mooncake-304003.misc.coca-cola` 
    VALUES
        ({}, CURRENT_DATETIME("America/Sao_Paulo"), {}, "{}")
    """.format(value, user_id, username))

    return '{} successfully inserted {} ml!'.format(username, value)


def aggregate(message):
    """Function to check the sum of ingested coke grouped by periodicity.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg: Query result - to be displayed at Telegram's chat.

    """
    helpers.set_path()
    client = helpers.start_connection()

    query_dict = {
        'day': """
            SELECT
                USERNAME,
                SUM(MILLILITERS) AS SUMMARY,
                MIN(DATETIME) AS DATETIME,
                CONCAT(EXTRACT(YEAR FROM DATETIME), 
                "-", EXTRACT(MONTH FROM DATETIME),
                 "-", EXTRACT(DAY FROM DATETIME)) AS SAFRA
            FROM
                `mooncake-304003.misc.coca-cola`
            WHERE
                USER_ID = {}
            GROUP BY
                SAFRA,
                USERNAME
            ORDER BY 
                DATETIME DESC
        """,
        'week': """
            SELECT
                USERNAME,
                SUM(MILLILITERS) AS SUMMARY,
                MIN(DATETIME) AS DATETIME,
                CONCAT(EXTRACT(YEAR FROM DATETIME), 
                "-", EXTRACT(WEEK FROM DATETIME)) AS SAFRA
            FROM
                `mooncake-304003.misc.coca-cola`
            WHERE
                USER_ID = {}
            GROUP BY
                SAFRA,
                USERNAME
            ORDER BY 
                DATETIME DESC
        """,
        'month': """
            SELECT
                USERNAME,
                SUM(MILLILITERS) AS SUMMARY,
                MIN(DATETIME) AS DATETIME,
                CONCAT(EXTRACT(YEAR FROM DATETIME), 
                "-", EXTRACT(MONTH FROM DATETIME)) AS SAFRA
            FROM
                `mooncake-304003.misc.coca-cola`
            WHERE
                USER_ID = {}
            GROUP BY
                SAFRA,
                USERNAME
            ORDER BY 
                DATETIME DESC
        """,
        'quarter': """
            SELECT
                USERNAME,
                SUM(MILLILITERS) AS SUMMARY,
                MIN(DATETIME) AS DATETIME,
                CONCAT(EXTRACT(YEAR FROM DATETIME), 
                "-", EXTRACT(QUARTER FROM DATETIME)) AS SAFRA
            FROM
                `mooncake-304003.misc.coca-cola`
            WHERE
                USER_ID = {}
            GROUP BY
                SAFRA,
                USERNAME
            ORDER BY 
                DATETIME DESC
        """,
        'year': """
            SELECT
                USERNAME,
                SUM(MILLILITERS) AS SUMMARY,
                MIN(DATETIME) AS DATETIME,
                CONCAT(EXTRACT(YEAR FROM DATETIME)) AS SAFRA
            FROM
                `mooncake-304003.misc.coca-cola`
            WHERE
                USER_ID = {}
            GROUP BY
                SAFRA,
                USERNAME
            ORDER BY 
                DATETIME DESC
        """,
        'top': """
            SELECT
                USERNAME,
                SUM(MILLILITERS) AS SUMMARY
            FROM
                `mooncake-304003.misc.coca-cola`
            GROUP BY
                USERNAME
            ORDER BY
                SUMMARY DESC
        """
    }

    periodicity = message.text.lower().split(' ')[-1]

    user_id = message.from_user.id

    query_result = \
        [i for i in client.query(query_dict.get(periodicity).format(user_id))]

    top_drinkers = ''
    if periodicity == 'top':
        for row in query_result:
            top_drinkers += \
                '{}: {}\n'.format(row.values()[0], row.values()[1])
        return top_drinkers
    else:
        try:
            return 'In {}: {} ingested {} ml'.format(
                query_result[0].values()[3],
                query_result[0].values()[0],
                query_result[0].values()[1]
            )
        except IndexError:
            return 'Impossible, perhaps the archives are incomplete!'


def reset(message):
    """Function to reset all coke ingested by a user.

    Parameters
    ----------
    message : telebot.types.Message
        The message object.

    Returns
    -------
    msg: success message.

    """
    helpers.set_path()
    client = helpers.start_connection()

    client.query("""
    DELETE
    FROM
        `mooncake-304003.misc.coca-cola`
    WHERE
        USER_ID = {}
        """.format(message.from_user.id))

    return 'Statistics successfully reset!'


def drop(message):
    """Meme function - someday will be used to drop register in coke database.

    Parameters
    ----------
    message : str
        To be dropped register.

    Returns
    -------
    msg : str
        Random message.

    """
    return random.choice([
        'olha aqui, você é tão feio que a sua incubadora tinha insulfilm',
        'faz o seguinte, enfia um peixe no cu e diz que é sereia',
        'sabe o que você é? Um esqueleto movido a peido',
        'você é tão burro que reprovou o exame de fezes',
        'vai cagar na praia e limpar o cú com ostras',
        'sua certidão de nascimento é um pedido de desculpas da fábrica de preservativos',
        'vai vender cocada no inferno',
        'você é tão feio que parece que foi feito pelo cú com rola mole',
        'sai daqui cavalo da carroça do faraó',
        'sai daqui paquita do capeta',
        'você é mais indigeto que bife de rato',
        'cansei de você seu saco de vacilo',
        'aff, la vem o sofá de zona',
        'que saco, vai lá coçar o cú com serrote',
        'voê é pacote completo né, além de lixo é um saco!'
        'va se lascar rapaz',
        'vai dar meia hora de cú com relógio parado',
        'vai ver se eu to na esquina',
        'você é burro cara!',
        'da licença o lustrador de palio de carne',
        'vai se lascar',
        'se o riso é o melhor remédio, seu rosto deve estar curando o mundo.',
        'você é tão feia que assustou o banheiro.',
        'sua árvore genealógica deve ser um cacto porque todo mundo é um idiota.',
        'não, não estou insultando você, estou descrevendo você.',
        'é melhor deixar alguém pensar que você é um idiota do que abrir a boca e provar isso.',
        'se eu tivesse um rosto como o seu, processaria meus pais.',
        'sua certidão de nascimento é uma carta de desculpas da fábrica de preservativos.',
        'eu acho que você prova que até deus comete erros às vezes.',
        'a única maneira que você vai se deitar é se você se arrepiar e esperar.',
        'você é tão falsa, barbie está com ciúmes.',
        'tenho inveja de pessoas que não te conhecem!',
        'meu psiquiatra me disse que eu era louco e disse que queria uma segunda opinião. ele disse que tudo bem, você é feia também.',
        'você é tão feia, quando sua mãe deixou você na escola, ela teve uma multa por jogar lixo.',
        'se eu quisesse me matar, escalaria seu ego e saltaria para o seu qi.',
        'você deve ter nascido em uma estrada porque é onde a maioria dos acidentes acontece.',
        'cérebros não são tudo. no seu caso, eles são nada.',
        'eu não sei o que te faz tão idiota, mas realmente funciona.',
        'eu posso explicar para você, mas não consigo entender para você.',
        'rosas são violetas vermelhas são azuis, deus me fez bonita, o que aconteceu com você?',
        'atrás de toda mulher gorda há uma mulher bonita. não a sério, você está no caminho.',
        'chamar você de idiota seria um insulto para todas as pessoas estúpidas.',
        'você, senhor, é um ladrão de oxigênio!',
        'alguns bebês foram jogados em suas cabeças, mas você foi claramente jogado em uma parede.',
        'não gosto do meu sarcasmo, bem, eu não gosto da sua estupidez.',
        'por que você não joga no trânsito?',
        'por favor, cale a boca quando estiver falando comigo.',
        'eu te bato, mas isso seria abuso animal.',
        'eles dizem que os opostos se atraem. espero que você conheça alguém que seja bonito, inteligente e culto.',
        'pare de tentar ser um espertinho, você é só um idiota.',
        'a última vez que vi algo parecido com você, corei.',
        'estou ocupado agora. posso te ignorar outra hora?',
        'você tem diarréia da boca; constipação das idéias.',
        'se o feio fosse um crime, você teria uma sentença de prisão perpétua.',
        'sua mente está de férias, mas sua boca está fazendo hora extra.',
        'eu posso perder peso, mas você sempre será feia.',
        'choca-me, diga algo inteligente.',
        'se você vai ter duas caras, mel, pelo menos, faça uma delas bonita.',
        'continue revirando os olhos, talvez você encontre um cérebro lá atrás.',
        'você não é tão ruim quanto as pessoas dizem, você é muito, muito pior.',
        'eu não sei qual é o seu problema, mas aposto que é difícil pronunciar.',
        'você ganha dez vezes mais garotas do que eu? dez vezes zero é zero ...',
        'não há vacina contra a estupidez.',
        'você é a razão pela qual o pool genético precisa de um salva-vidas.',
        'claro, eu vi pessoas como você antes - mas eu tive que pagar uma admissão.',
        'quantos anos você tem? - espere, eu não deveria perguntar, você não pode contar tão alto assim.',
        'você tem comprado ultimamente? eles estão vendendo vidas, você deveria comprar um.',
        'você é como as manhãs de segunda-feira, ninguém gosta de você.',
        'claro que eu falo como um idiota, o que mais você me entende?',
        'todo dia eu pensei em você ... eu estava no zoológico.',
        'para fazer você rir no sábado, eu preciso de você piada na quarta-feira.',
        'você é tão gordo, você poderia vender sombra.',
        'eu gostaria de ver as coisas do seu ponto de vista, mas eu não consigo entender minha cabeça tão alto.',
        'você não precisa de uma licença para ser tão feia?',
        'meu amigo acha que ele é esperto. ele me disse que uma cebola é a única comida que faz você chorar, então eu joguei um coco no rosto dele.',
        'sua casa está tão suja que você tem que limpar os pés antes de sair.',
        'se você realmente falava sua mente, ficaria sem fala.',
        'a estupidez não é um crime, então você está livre para ir.',
        'você é tão velho, quando você era criança arco-íris eram preto e branco.',
        'se eu te dissesse que tenho um pedaço de sujeira no meu olho, você se mexeria?',
        'você é tão burro, você acha que as cheerios são sementes de donut.',
        'então, um pensamento passou pela sua cabeça? deve ter sido uma jornada longa e solitária.',
        'você é tão velho, seu certificado de nascimento expirou.',
        'toda vez que estou ao seu lado, tenho um forte desejo de ficar sozinha.',
        'você é tão burro que foi atropelado por um carro estacionado.',
        'continue falando, algum dia você dirá algo inteligente!',
        'você é tão gordo que deixa pegadas no concreto.',
        'como você chegou aqui? alguém deixou sua gaiola aberta?',
        'perdoe-me, mas você obviamente me confundiu com alguém que se importa.',
        'limpe sua boca, ainda há um pouquinho de besteira em volta dos seus lábios.',
        'você não tem um sentimento terrivelmente vazio - no seu crânio?',
        'como um estranho, o que você acha da raça humana?',
        'só porque você tem um não significa que você tem que agir como um.',
        'nós sempre podemos dizer quando você está mentindo. seus lábios se movem.',
        'você é sempre tão estúpido ou hoje é uma ocasião especial?',
        'bota uma dentadura no cú e ri pro caralho',
    ])

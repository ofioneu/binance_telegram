
def register_step(message, msg, url_register):
    '''if msg != 'eth' or msg != 'btc':
    msg = bot.reply_to(message, 'Digite o simbolo da moeda ou retornar para voltar')
    bot.register_next_step_handler(msg, lucro)
    return'''
    if msg == 'retornar':
        bot.register_next_step_handler(message, send_welcome)   
    return


    if msg == 'btc':
        step_register(message, msg, url_register)


    if msg == 'eth':
        step_register(message, msg, url_register)

    if msg == 'bnb':
        step_register(message, msg, url_register)

    if msg == 'ada':
        step_register(message, msg, url_register)

    if msg == 'chz':
        step_register(message, msg, url_register)

    if msg == 'ustd':
        step_register(message, msg, url_register) 

    if msg == 'busd':
        step_register(message, msg, url_register)

    if msg == '1inch':
        step_register(message, msg, url_register)

    if msg == 'aave':
        step_register(message, msg, url_register)

    if msg == 'algo':
        step_register(message, msg, url_register)

    if msg == 'ankr':
        step_register(message, msg, url_register)

    if msg == 'ardr':
        step_register(message, msg, url_register)

    if msg == 'atom':
        step_register(message, msg, url_register)

    if msg == 'ava':
        step_register(message, msg, url_register)

    if msg == 'bake':
        step_register(message, msg, url_register)

    if msg == 'bat':
        step_register(message, msg, url_register)

    if msg == 'bch':
        step_register(message, msg, url_register)

    if msg == 'btt':
        step_register(message, msg, url_register)

    if msg == 'cake':
        step_register(message, msg, url_register)

    if msg == 'chr':
        step_register(message, msg, url_register)
    
    if msg == 'comp':
        step_register(message, msg, url_register)

    if msg == 'dai':
        step_register(message, msg, url_register)

    if msg == 'dash':
        step_register(message, msg, url_register)

    if msg == 'doge':
        step_register(message, msg, url_register)

    if msg == 'dot':
        step_register(message, msg, url_register)

    if msg == 'egld':
        step_register(message, msg, url_register)

    if msg == 'enj':
        step_register(message, msg, url_register)

    if msg == 'eos':
        step_register(message, msg, url_register)

    if msg == 'etc':
        step_register(message, msg, url_register)

    if msg == 'fil':
        step_register(message, msg, url_register)

    if msg == 'fio':
        step_register(message, msg, url_register)

    if msg == 'ftm':
        step_register(message, msg, url_register)

    if msg == 'grt':
        step_register(message, msg, url_register)

    if msg == 'iota':
        step_register(message, msg, url_register)

    if msg == 'link':
        step_register(message, msg, url_register)

    if msg == 'ltc':
        step_register(message, msg, url_register)

    if msg == 'luna':
        step_register(message, msg, url_register)

    if msg == 'mana':
        step_register(message, msg, url_register)

    if msg == 'matic':
        step_register(message, msg, url_register)

    if msg == 'mkr':
        step_register(message, msg, url_register)

    if msg == 'neo':
        step_register(message, msg, url_register)

    if msg == 'rune':
        step_register(message, msg, url_register)

    if msg == 'shib':
        step_register(message, msg, url_register)

    if msg == 'snx':
        step_register(message, msg, url_register)

    if msg == 'sol':
        step_register(message, msg, url_register) 

    if msg == 'sxp':
        step_register(message, msg, url_register)

    if msg == 'theta':
        step_register(message, msg, url_register)

    if msg == 'trx':
        step_register(message, msg, url_register)

    if msg == 'uni':
        step_register(message, msg, url_register)

    if msg == 'vet':
        step_register(message, msg, url_register)

    if msg == 'waves':
        step_register(message, msg, url_register)
    
    if msg == 'win':
        step_register(message, msg, url_register)

    if msg == 'wxr':
        step_register(message, msg, url_register)

    if msg == 'xem':
        step_register(message, msg, url_register)

    if msg == 'xlm':
        step_register(message, msg, url_register)

    if msg == 'xrp':
        step_register(message, msg, url_register)

    if msg == 'xtz':
        step_register(message, msg, url_register)

    if msg == 'yfi':
        step_register(message, msg, url_register)

    if msg == 'zec':
        step_register(message, msg, url_register)

    if msg == 'zil':
        step_register(message, msg, url_register)

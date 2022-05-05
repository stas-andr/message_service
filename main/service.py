def post_save_maillist(sender, **kwargs):
    if kwargs['created']:
        print('Рассылка %s создана' % kwargs['instance'].name)
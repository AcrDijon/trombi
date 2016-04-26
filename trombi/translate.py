# coding: utf8

_TRANSLATIONS = {
    'is_published': u'Publier les infos',
    'bio': u'Ma biographie',
    'email': u'Couriel',
    'phone': u'Téléphone',
    'address' : u'Adresse',
    'city': u'Ville',
    'category': u'Catégorie',
    'membership': u'Type adhésion',
    'permissions': u'Permissions',
    'lastname': u'Nom',
    'firstname': u'Prénom',
    'password': u'Mot de passe',
    'licence': u'NºLicence',
    'gender': u'Sexe',
    'birthday': u'Date de Naissance',
    'medical_certificate_date': u'Date certificat médical',
    'has_paid': u'Paiement à jour',
    'last_updated': u'Date infos à jour'
}


def _(text):
    return _TRANSLATIONS.get(text, text)

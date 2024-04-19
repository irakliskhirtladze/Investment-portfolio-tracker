# Generated by Django 5.0.3 on 2024-04-18 12:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateField(auto_now=True, verbose_name='Date Modified')),
                ('instrument_type', models.CharField(choices=[('stocks', 'Stocks'), ('crypto', 'Crypto'), ('cash', 'Cash')], max_length=10, verbose_name='Instrument Type')),
                ('instrument_symbol', models.CharField(max_length=10, verbose_name='Symbol')),
                ('instrument_name', models.CharField(max_length=100, verbose_name='Instrument Name')),
                ('trade_currency', models.CharField(choices=[('AFN', 'Afghani'), ('EUR', 'Euro'), ('ALL', 'Lek'), ('DZD', 'Algerian Dinar'), ('USD', 'US Dollar'), ('AOA', 'Kwanza'), ('XCD', 'East Caribbean Dollar'), ('ARS', 'Argentine Peso'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Florin'), ('AUD', 'Australian Dollar'), ('AZN', 'Azerbaijan Manat'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('BDT', 'Taka'), ('BBD', 'Barbados Dollar'), ('BYN', 'Belarusian Ruble'), ('BZD', 'Belize Dollar'), ('XOF', 'CFA Franc BCEAO'), ('BMD', 'Bermudian Dollar'), ('INR', 'Indian Rupee'), ('BTN', 'Ngultrum'), ('BOB', 'Boliviano'), ('BAM', 'Convertible Mark'), ('BWP', 'Pula'), ('NOK', 'Norwegian Krone'), ('BRL', 'Brazilian Real'), ('BND', 'Brunei Dollar'), ('BGN', 'Bulgarian Lev'), ('BIF', 'Burundi Franc'), ('CVE', 'Cabo Verde Escudo'), ('KHR', 'Riel'), ('XAF', 'CFA Franc BEAC'), ('CAD', 'Canadian Dollar'), ('KYD', 'Cayman Islands Dollar'), ('CLP', 'Chilean Peso'), ('CNY', 'Yuan Renminbi'), ('COP', 'Colombian Peso'), ('KMF', 'Comorian Franc '), ('CDF', 'Congolese Franc'), ('NZD', 'New Zealand Dollar'), ('CRC', 'Costa Rican Colon'), ('CUP', 'Cuban Peso'), ('CUC', 'Peso Convertible'), ('ANG', 'Netherlands Antillean Guilder'), ('CZK', 'Czech Koruna'), ('DKK', 'Danish Krone'), ('DJF', 'Djibouti Franc'), ('DOP', 'Dominican Peso'), ('EGP', 'Egyptian Pound'), ('SVC', 'El Salvador Colon'), ('ERN', 'Nakfa'), ('SZL', 'Lilangeni'), ('ETB', 'Ethiopian Birr'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fiji Dollar'), ('XPF', 'CFP Franc'), ('GMD', 'Dalasi'), ('GEL', 'Lari'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('GTQ', 'Quetzal'), ('GBP', 'Pound Sterling'), ('GNF', 'Guinean Franc'), ('GYD', 'Guyana Dollar'), ('HTG', 'Gourde'), ('HNL', 'Lempira'), ('HKD', 'Hong Kong Dollar'), ('HUF', 'Forint'), ('ISK', 'Iceland Krona'), ('IDR', 'Rupiah'), ('XDR', 'SDR (Special Drawing Right)'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('ILS', 'New Israeli Sheqel'), ('JMD', 'Jamaican Dollar'), ('JPY', 'Yen'), ('JOD', 'Jordanian Dinar'), ('KZT', 'Tenge'), ('KES', 'Kenyan Shilling'), ('KPW', 'North Korean Won'), ('KRW', 'Won'), ('KWD', 'Kuwaiti Dinar'), ('KGS', 'Som'), ('LAK', 'Lao Kip'), ('LBP', 'Lebanese Pound'), ('LSL', 'Loti'), ('ZAR', 'Rand'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('CHF', 'Swiss Franc'), ('MOP', 'Pataca'), ('MKD', 'Denar'), ('MGA', 'Malagasy Ariary'), ('MWK', 'Malawi Kwacha'), ('MYR', 'Malaysian Ringgit'), ('MVR', 'Rufiyaa'), ('MRU', 'Ouguiya'), ('MUR', 'Mauritius Rupee'), ('XUA', 'ADB Unit of Account'), ('MXN', 'Mexican Peso'), ('MDL', 'Moldovan Leu'), ('MNT', 'Tugrik'), ('MAD', 'Moroccan Dirham'), ('MZN', 'Mozambique Metical'), ('MMK', 'Kyat'), ('NAD', 'Namibia Dollar'), ('NPR', 'Nepalese Rupee'), ('NIO', 'Cordoba Oro'), ('NGN', 'Naira'), ('OMR', 'Rial Omani'), ('PKR', 'Pakistan Rupee'), ('PAB', 'Balboa'), ('PGK', 'Kina'), ('PYG', 'Guarani'), ('PEN', 'Sol'), ('PHP', 'Philippine Peso'), ('PLN', 'Zloty'), ('QAR', 'Qatari Rial'), ('RON', 'Romanian Leu'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('SHP', 'Saint Helena Pound'), ('WST', 'Tala'), ('STN', 'Dobra'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('SCR', 'Seychelles Rupee'), ('SLE', 'Leone'), ('SGD', 'Singapore Dollar'), ('XSU', 'Sucre'), ('SBD', 'Solomon Islands Dollar'), ('SOS', 'Somali Shilling'), ('SSP', 'South Sudanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('SDG', 'Sudanese Pound'), ('SRD', 'Surinam Dollar'), ('SEK', 'Swedish Krona'), ('SYP', 'Syrian Pound'), ('TWD', 'New Taiwan Dollar'), ('TJS', 'Somoni'), ('TZS', 'Tanzanian Shilling'), ('THB', 'Baht'), ('TOP', 'Pa’anga'), ('TTD', 'Trinidad and Tobago Dollar'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TMT', 'Turkmenistan New Manat'), ('UGX', 'Uganda Shilling'), ('UAH', 'Hryvnia'), ('AED', 'UAE Dirham'), ('UYU', 'Peso Uruguayo'), ('UYW', 'Unidad Previsional'), ('UZS', 'Uzbekistan Sum'), ('VUV', 'Vatu'), ('VES', 'Bolívar Soberano'), ('VED', 'Bolívar Soberano'), ('VND', 'Dong'), ('YER', 'Yemeni Rial'), ('ZMW', 'Zambian Kwacha'), ('ZWL', 'Zimbabwe Dollar')], max_length=5, verbose_name='Currency')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Instrument Quantity')),
                ('average_trade_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Trade Price')),
                ('commissions', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Commission')),
                ('cost_basis', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cost Basis')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Portfolio Entry',
                'verbose_name_plural': 'Portfolio Entries',
            },
        ),
        migrations.CreateModel(
            name='PortfolioSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snapshot_date', models.DateField(auto_now=True, verbose_name='Snapshot Date')),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Current Price')),
                ('current_value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Current Value')),
                ('profit_loss', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Profit/Loss')),
                ('profit_loss_percent', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Profit/Loss %')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolioentry', verbose_name='Portfolio Entry')),
            ],
            options={
                'verbose_name': 'Portfolio Snapshot',
                'verbose_name_plural': 'Portfolio Snapshots',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(auto_now=True, verbose_name='Transaction Date')),
                ('instrument_type', models.CharField(choices=[('stocks', 'Stocks'), ('crypto', 'Crypto'), ('cash', 'Cash')], max_length=10, verbose_name='Instrument Type')),
                ('instrument_symbol', models.CharField(max_length=10, verbose_name='Symbol')),
                ('instrument_name', models.CharField(max_length=100, verbose_name='Instrument Name')),
                ('transaction_currency', models.CharField(choices=[('AFN', 'Afghani'), ('EUR', 'Euro'), ('ALL', 'Lek'), ('DZD', 'Algerian Dinar'), ('USD', 'US Dollar'), ('AOA', 'Kwanza'), ('XCD', 'East Caribbean Dollar'), ('ARS', 'Argentine Peso'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Florin'), ('AUD', 'Australian Dollar'), ('AZN', 'Azerbaijan Manat'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('BDT', 'Taka'), ('BBD', 'Barbados Dollar'), ('BYN', 'Belarusian Ruble'), ('BZD', 'Belize Dollar'), ('XOF', 'CFA Franc BCEAO'), ('BMD', 'Bermudian Dollar'), ('INR', 'Indian Rupee'), ('BTN', 'Ngultrum'), ('BOB', 'Boliviano'), ('BAM', 'Convertible Mark'), ('BWP', 'Pula'), ('NOK', 'Norwegian Krone'), ('BRL', 'Brazilian Real'), ('BND', 'Brunei Dollar'), ('BGN', 'Bulgarian Lev'), ('BIF', 'Burundi Franc'), ('CVE', 'Cabo Verde Escudo'), ('KHR', 'Riel'), ('XAF', 'CFA Franc BEAC'), ('CAD', 'Canadian Dollar'), ('KYD', 'Cayman Islands Dollar'), ('CLP', 'Chilean Peso'), ('CNY', 'Yuan Renminbi'), ('COP', 'Colombian Peso'), ('KMF', 'Comorian Franc '), ('CDF', 'Congolese Franc'), ('NZD', 'New Zealand Dollar'), ('CRC', 'Costa Rican Colon'), ('CUP', 'Cuban Peso'), ('CUC', 'Peso Convertible'), ('ANG', 'Netherlands Antillean Guilder'), ('CZK', 'Czech Koruna'), ('DKK', 'Danish Krone'), ('DJF', 'Djibouti Franc'), ('DOP', 'Dominican Peso'), ('EGP', 'Egyptian Pound'), ('SVC', 'El Salvador Colon'), ('ERN', 'Nakfa'), ('SZL', 'Lilangeni'), ('ETB', 'Ethiopian Birr'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fiji Dollar'), ('XPF', 'CFP Franc'), ('GMD', 'Dalasi'), ('GEL', 'Lari'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('GTQ', 'Quetzal'), ('GBP', 'Pound Sterling'), ('GNF', 'Guinean Franc'), ('GYD', 'Guyana Dollar'), ('HTG', 'Gourde'), ('HNL', 'Lempira'), ('HKD', 'Hong Kong Dollar'), ('HUF', 'Forint'), ('ISK', 'Iceland Krona'), ('IDR', 'Rupiah'), ('XDR', 'SDR (Special Drawing Right)'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('ILS', 'New Israeli Sheqel'), ('JMD', 'Jamaican Dollar'), ('JPY', 'Yen'), ('JOD', 'Jordanian Dinar'), ('KZT', 'Tenge'), ('KES', 'Kenyan Shilling'), ('KPW', 'North Korean Won'), ('KRW', 'Won'), ('KWD', 'Kuwaiti Dinar'), ('KGS', 'Som'), ('LAK', 'Lao Kip'), ('LBP', 'Lebanese Pound'), ('LSL', 'Loti'), ('ZAR', 'Rand'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('CHF', 'Swiss Franc'), ('MOP', 'Pataca'), ('MKD', 'Denar'), ('MGA', 'Malagasy Ariary'), ('MWK', 'Malawi Kwacha'), ('MYR', 'Malaysian Ringgit'), ('MVR', 'Rufiyaa'), ('MRU', 'Ouguiya'), ('MUR', 'Mauritius Rupee'), ('XUA', 'ADB Unit of Account'), ('MXN', 'Mexican Peso'), ('MDL', 'Moldovan Leu'), ('MNT', 'Tugrik'), ('MAD', 'Moroccan Dirham'), ('MZN', 'Mozambique Metical'), ('MMK', 'Kyat'), ('NAD', 'Namibia Dollar'), ('NPR', 'Nepalese Rupee'), ('NIO', 'Cordoba Oro'), ('NGN', 'Naira'), ('OMR', 'Rial Omani'), ('PKR', 'Pakistan Rupee'), ('PAB', 'Balboa'), ('PGK', 'Kina'), ('PYG', 'Guarani'), ('PEN', 'Sol'), ('PHP', 'Philippine Peso'), ('PLN', 'Zloty'), ('QAR', 'Qatari Rial'), ('RON', 'Romanian Leu'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('SHP', 'Saint Helena Pound'), ('WST', 'Tala'), ('STN', 'Dobra'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('SCR', 'Seychelles Rupee'), ('SLE', 'Leone'), ('SGD', 'Singapore Dollar'), ('XSU', 'Sucre'), ('SBD', 'Solomon Islands Dollar'), ('SOS', 'Somali Shilling'), ('SSP', 'South Sudanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('SDG', 'Sudanese Pound'), ('SRD', 'Surinam Dollar'), ('SEK', 'Swedish Krona'), ('SYP', 'Syrian Pound'), ('TWD', 'New Taiwan Dollar'), ('TJS', 'Somoni'), ('TZS', 'Tanzanian Shilling'), ('THB', 'Baht'), ('TOP', 'Pa’anga'), ('TTD', 'Trinidad and Tobago Dollar'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TMT', 'Turkmenistan New Manat'), ('UGX', 'Uganda Shilling'), ('UAH', 'Hryvnia'), ('AED', 'UAE Dirham'), ('UYU', 'Peso Uruguayo'), ('UYW', 'Unidad Previsional'), ('UZS', 'Uzbekistan Sum'), ('VUV', 'Vatu'), ('VES', 'Bolívar Soberano'), ('VED', 'Bolívar Soberano'), ('VND', 'Dong'), ('YER', 'Yemeni Rial'), ('ZMW', 'Zambian Kwacha'), ('ZWL', 'Zimbabwe Dollar')], max_length=5, verbose_name='Currency')),
                ('transaction_type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell'), ('dividend', 'Dividend')], max_length=10, verbose_name='Transaction Type')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Quantity')),
                ('trade_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Trade Price')),
                ('commission', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Commission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(LanguageDetector)
  // pass the i18n instance to react-i18next.
  .use(initReactI18next)
  .init({
    debug: true,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    },
    resources: {
      en: {
        translation: {
          appbar: {
            appmenu: {
              accounts: 'Accounts',
              categories: 'Categories',
              import: 'Import',
              export: 'Export',
              settings: 'Settings',
            }
          },
          transactions: {
            title: 'Transactions',
            add: 'Add',
            edit: 'Edit',
            delete: 'Delete',
          },
          labels: {
            account: 'Account',
            category: 'Category',
            amount: 'Amount',
            bank: 'Bank',
          },
          error: 'Error',
         success: 'Sucess'

        },
      },
      ptBr: {
        translation: {
          appbar: {
            appmenu: {
              accounts: 'Contas',
              categories: 'Categorias',
              import: 'Importar',
              export: 'Exportar',
              settings: 'Configurações',
            }
          },
          transactions: {
            title: 'Transações',
            add: 'Adicionar',
            edit: 'Editar',
            delete: 'Excluir',
          },
          labels: {
            account: 'Conta',
            category: 'Categoria',
            amount: 'Quantia',
            bank: 'Banco',
        },
         error: 'Erro',
         success: 'Sucesso'
        }
      }
    }
  })


export default i18n;
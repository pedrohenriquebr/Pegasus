import { useEffect, useState } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import Spinner from 'react-bootstrap/Spinner';
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import filterFactory, { textFilter, numberFilter, dateFilter, } from 'react-bootstrap-table2-filter';
import api from '../../../services/api';
import './index.css';




export default function Grid({ accountId }) {

  const [data, setData] = useState([]);
  const [isLoading, setLoading] = useState(true);
  useEffect(() => {
    setData([])
    setLoading(true);
    api.post('/transactions/get-all', {
      "id_account": accountId,
      "limit": -1
    }).then(d => {
      setData(d.data.data)
      setLoading(false)
    })
  }, [accountId])


  const headerSortingClasses = (column, sortOrder, isLastSorting, colIndex) => (
    sortOrder === 'asc' ? 'demo-sorting-asc' : 'demo-sorting-desc'
  );
  const headerStyle = (colum, colIndex) => {
    return { width: '200px', textAlign: 'center' };
  }

  const NoDataIndication = () => {
    return isLoading ? <Spinner animation="border" variant="primary" /> : <p> Empty </p>
  }

  const columns = [
    { sort: true, headerStyle: headerStyle, filter: numberFilter(), headerSortingClasses, type: "number", dataField: 'id', text: 'ID_Transaction', },
    { sort: true, headerStyle: headerStyle, headerSortingClasses, type: "bool", dataField: 'is_imported', text: 'IC_Imported', },
    { sort: true, headerStyle: headerStyle, filter: textFilter(), headerSortingClasses, type: "string", dataField: 'account', text: 'Account', },
    { sort: true, headerStyle: headerStyle, filter: textFilter(), headerSortingClasses, type: "string", dataField: 'account_destination', text: 'Account Destination', },
    { sort: true, headerStyle: headerStyle, filter: textFilter(), headerSortingClasses, type: "string", dataField: 'type', text: 'CD_Type', type: 'string', width: 100 },
    { sort: true, headerStyle: headerStyle, filter: textFilter(), headerSortingClasses, type: "string", dataField: 'category', text: 'Category', },
    { sort: true, headerStyle: headerStyle, filter: dateFilter(), headerSortingClasses, type: "date", dataField: 'transaction_date', text: 'DT_TransactionDate', },
    { sort: true, headerStyle: headerStyle, filter: dateFilter(), headerSortingClasses, type: "date", dataField: 'registration_date', text: 'DT_RegistrationDate', },
    { sort: true, headerStyle: headerStyle, filter: numberFilter(), headerSortingClasses, type: "number", dataField: 'amount', text: 'Amount', },
    { sort: true, headerStyle: headerStyle, filter: textFilter(), headerSortingClasses, type: "string", dataField: 'description', text: 'DS_Description', },
    { sort: true, headerStyle: headerStyle, filter: textFilter(), headerSortingClasses, type: "string", dataField: 'attachment_details', text: 'DS_AttachmentDetails', },
    { sort: true, headerStyle: headerStyle, filter: textFilter(), headerSortingClasses, type: "string", dataField: 'attachment_path', text: 'AttachmentPath', },
    { sort: true, headerStyle: headerStyle, filter: dateFilter(), headerSortingClasses, type: "date", dataField: 'imported_date', text: 'ImportedDate', },
    { sort: true, headerStyle: headerStyle, filter: numberFilter(), headerSortingClasses, type: "number", dataField: 'balance', text: 'NR_Balance', },
  ];

  return (

    <PaginationProvider
      pagination={paginationFactory({ custom: true, totalSize: data.length })}
    >
      {
        ({
          paginationProps,
          paginationTableProps
        }) => (
          <div>
            <PaginationListStandalone
              {...paginationProps}
            />
            <div className="table-container">
              <BootstrapTable
                keyField="id"
                striped
                hover
                condensed
                tabIndexCell
                pagination={paginationFactory()}
                data={data}
                columns={columns}
                noDataIndication={() => <NoDataIndication />}
                {...paginationTableProps}
                filter={filterFactory()}
              />
            </div>
          </div>
        )
      }
    </PaginationProvider >
  )


}
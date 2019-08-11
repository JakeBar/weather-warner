import React from 'react'
import ReactDOM from 'react-dom'
import { AppContainer } from 'react-hot-loader'
import axios from 'axios'
import FormContainer from './components/FormContainer'

// Default Config
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

// Initial Load
ReactDOM.render(
  <AppContainer>
    <FormContainer />
  </AppContainer>,
  document.getElementById('root')
)

// React Hot Loader
// https://github.com/gaearon/react-hot-loader
if (module.hot) {
  ReactDOM.render(
    <AppContainer>
      <FormContainer />
    </AppContainer>,
    document.getElementById('root')
  )
}

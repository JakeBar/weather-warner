import React from 'react'
import ReactDOM from 'react-dom'
import { AppContainer } from 'react-hot-loader'
import axios from 'axios'
import Container from './components/Container'

// Default Config
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'

// Initial Load
ReactDOM.render(
  <AppContainer>
    <Container />
  </AppContainer>,
  document.getElementById('root')
)

// React Hot Loader
// https://github.com/gaearon/react-hot-loader
if (module.hot) {
  ReactDOM.render(
    <AppContainer>
      <Container />
    </AppContainer>,
    document.getElementById('root')
  )
}

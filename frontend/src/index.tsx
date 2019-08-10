import React from 'react'
import ReactDOM from 'react-dom'
import { AppContainer } from 'react-hot-loader'
import FormContainer from './components/FormContainer'

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

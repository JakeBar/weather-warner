import React from 'react'
import { Header } from 'semantic-ui-react'

const AppHeader = () => (
  <Header style={{ color: 'white' }} as="h2" textAlign="center">
    Sign up for Weather Warner
    <Header.Subheader style={{ color: 'white' }}>
      SMS forecasts straight to your phone.
    </Header.Subheader>
  </Header>
)

export default AppHeader

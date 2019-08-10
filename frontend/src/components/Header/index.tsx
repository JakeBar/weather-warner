import React from 'react'
import { Header as SemanticHeader } from 'semantic-ui-react'

const Header = () => (
  <SemanticHeader style={{ color: 'white' }} as="h2" textAlign="center">
    Sign up for Weather Warner
    <SemanticHeader.Subheader style={{ color: 'white' }}>
      SMS forecasts straight to your phone.
    </SemanticHeader.Subheader>
  </SemanticHeader>
)

export default Header

import React from 'react'
import { Segment, Icon } from 'semantic-ui-react'

const Footer = () => (
  <Segment basic style={{ height: '5vh' }} textAlign="right" as="footer">
    <a
      style={{ color: 'white' }}
      href="https://github.com/JakeBar/weather-warner"
      target="_blank"
      rel="noopener noreferrer"
    >
      github.com/jakebar <Icon fitted name="github" />
    </a>
  </Segment>
)

export default Footer

/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React, { PureComponent, Fragment } from 'react'
import { Input, Container, Segment, Grid, Header, Form, Button, Icon } from 'semantic-ui-react'

const SignUpForm = () => (
  <Grid textAlign="center" style={{ height: '95vh' }} verticalAlign="middle">
    <Grid.Column textAlign="left" style={{ maxWidth: 400 }}>
      <Header style={{ color: 'white' }} as="h2" textAlign="center">
        Sign up for Weather Warner
        <Header.Subheader style={{ color: 'white' }}>
          SMS forecasts straight to your phone.
        </Header.Subheader>
      </Header>

      <Form size="large">
        <Segment style={{ backgroundColor: 'transparent', border: 'none', boxShadow: 'none' }}>
          <Form.Field fluid type="text">
            <label style={{ color: 'white' }}>First name</label>
            <Input placeholder="Mister Monday" type="text" />
          </Form.Field>
          <Form.Field fluid>
            <label style={{ color: 'white' }}>Phone Number</label>
            <Input placeholder="+614 21 222 333" icon="phone" iconPosition="left" type="tel" />
          </Form.Field>
          <Form.Field fluid>
            <label style={{ color: 'white' }}>Postcode</label>
            <Input
              placeholder='"e.g. 3000'
              icon="compass outline"
              iconPosition="left"
              type="text"
            />
          </Form.Field>

          <Button
            style={{ border: '1px solid white', backgroundColor: 'transparent', color: 'white' }}
            fluid
            size="large"
          >
            Verify Number
          </Button>
        </Segment>
      </Form>
    </Grid.Column>
  </Grid>
)

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

class FormContainer extends PureComponent {
  render() {
    return (
      <Fragment>
        <Container>
          <SignUpForm />
          <Footer />
        </Container>
      </Fragment>
    )
  }
}

export default FormContainer

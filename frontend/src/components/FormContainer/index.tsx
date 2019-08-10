/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React, { useState, Fragment } from 'react'
import { Container, Segment, Grid, Form, Message } from 'semantic-ui-react'
import axios from 'axios'
import Footer from '../Footer'
import AppHeader from '../AppHeader'
import useSignUpForm from './hooks'
import { ApplicationState, ErrorValues, FormValues } from './types'
import VerificationForm from '../VerificationForm'

interface SignUpFormProps {
  submitDetails: Function
  formErrors: ErrorValues
}

const SignUpForm = (props: SignUpFormProps) => {
  const verifyDetails = () => {
    props.submitDetails(formValues)
  }

  const { formValues, handleFormValues, handleSubmit } = useSignUpForm(verifyDetails)

  const { formErrors } = props

  const nameErrors = formErrors.name ? { error: formErrors.name } : {}
  const phoneNumberErrors = formErrors.phone_number ? { error: formErrors.phone_number } : {}
  const postalCodeErrors = formErrors.postal_code ? { error: formErrors.postal_code } : {}

  return (
    <Form error={formErrors.general.length > 0} size="large" onSubmit={handleSubmit}>
      <Segment style={{ backgroundColor: 'transparent', border: 'none', boxShadow: 'none' }}>
        <Form.Field>
          <label style={{ color: 'white' }}>First name</label>
          <Form.Input
            {...nameErrors}
            placeholder="Mister Monday"
            name="name"
            type="text"
            required
            onChange={handleFormValues}
            value={formValues.name}
          />
        </Form.Field>

        <Form.Field>
          <label style={{ color: 'white' }}>Phone number</label>
          <Form.Input
            {...phoneNumberErrors}
            placeholder="+614 21 222 333"
            name="phone_number"
            type="tel"
            required
            onChange={handleFormValues}
            value={formValues.phone_number}
            icon="phone"
            iconPosition="left"
          />
        </Form.Field>
        <Form.Field>
          <label style={{ color: 'white' }}>Postcode</label>
          <Form.Input
            {...postalCodeErrors}
            placeholder='"e.g. 3000'
            name="postal_code"
            type="text"
            required
            onChange={handleFormValues}
            value={formValues.postal_code}
            icon="compass outline"
            iconPosition="left"
          />
        </Form.Field>

        {formErrors.general && <Message error content={formErrors.general} />}

        <Form.Button
          style={{ border: '1px solid white', backgroundColor: 'transparent', color: 'white' }}
          fluid
          size="large"
          type="submit"
        >
          Verify Number
        </Form.Button>
      </Segment>
    </Form>
  )
}

const SignUpSuccess = () => {
  return <div>You&apos;ve successfully signed up!</div>
}

const FormContainer = () => {
  const defaultProps = {
    submitted: false,
    verified: false,
    phone_number: '',
    formErrors: {
      general: '',
      name: '',
      phone_number: '',
      postal_code: '',
    },
  }
  const [state, setState] = useState<ApplicationState>(defaultProps)

  const requestVerification = (data: FormValues) => {
    axios
      .post('/api/verification/request/', data)
      .then(() => {
        setState({ ...state, submitted: true, phone_number: data.phone_number })
      })
      .catch(error => {
        if (error && error.response && error.response.status === 429) {
          const msg = 'Woah, slow down there! Try again later.'
          setState({
            ...state,
            formErrors: {
              ...state.formErrors,
              general: msg,
            },
          })
        } else if (error && error.response) {
          const msg = 'Please ensure all fields are correct.'
          setState({
            ...state,
            formErrors: {
              ...state.formErrors,
              ...error.response.data,
              general: msg,
            },
          })
        }
      })
  }

  let currentForm
  if (!state.submitted) {
    currentForm = <SignUpForm formErrors={state.formErrors} submitDetails={requestVerification} />
  } else if (!state.verified) {
    // currentForm = <VerificationForm phoneNumber={state.phone_number} />
    currentForm = <VerificationForm />
  } else if (state.verified) {
    currentForm = <SignUpSuccess />
  }

  return (
    <Fragment>
      <Container>
        <Grid textAlign="center" style={{ height: '95vh' }} verticalAlign="middle">
          <Grid.Column textAlign="left" style={{ maxWidth: 400 }}>
            <AppHeader />
            {currentForm}
          </Grid.Column>
        </Grid>
        <Footer />
      </Container>
    </Fragment>
  )
}

export default FormContainer

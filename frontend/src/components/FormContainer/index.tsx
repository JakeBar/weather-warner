/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React, { useState, Fragment } from 'react'
import { Container, Grid } from 'semantic-ui-react'
import axios from 'axios'
import Footer from '../Footer'
import Header from '../Header'
import SignUpForm from '../SignUpForm/index'
import { ApplicationState } from './types'
import { FormValues as SignUpFormValues } from '../SignUpForm/types'
import { FormValues as VerificationFormValues } from '../VerificationForm/types'
import VerificationForm from '../VerificationForm'
import SignUpSuccess from '../SignUpSuccess'

// eslint-disable-next-line
const camelize = require('camelize')

const FormContainer = () => {
  const defaultProps = {
    submitted: false,
    verified: false,
    formErrors: {
      general: '',
      name: '',
      phoneNumber: '',
      postalCode: '',
      verificationCode: '',
    },
  }
  const [state, setState] = useState<ApplicationState>(defaultProps)

  const requestVerification = (data: SignUpFormValues) => {
    const payload = {
      ...data,
      postal_code: data.postalCode,
      phone_number: data.phoneNumber,
    }
    axios
      .post('/api/verification/request/', payload)
      .then(() => {
        setState({
          ...state,
          submitted: true,
          formErrors: {
            ...defaultProps.formErrors,
          },
        })
      })
      .catch(error => {
        if (error && error.response && error.response.status === 429) {
          const msg = 'Woah, slow down there! Try again later.'
          setState({
            ...state,
            formErrors: {
              ...defaultProps.formErrors,
              general: msg,
            },
          })
        } else if (error && error.response) {
          const msg = 'Please ensure all fields are correct.'
          const formattedErrors = camelize(error.response.data)
          setState({
            ...state,
            formErrors: {
              ...defaultProps.formErrors,
              ...formattedErrors,
              general: msg,
            },
          })
        }
      })
  }

  const validateCode = (data: VerificationFormValues) => {
    const payload = {
      verification_code: data.verificationCode,
    }
    axios
      .post('/api/verification/validate/', payload)
      .then(() => {
        setState({ ...state, verified: true })
      })
      .catch(error => {
        if (error && error.response && error.response.status === 429) {
          const msg = 'Woah, slow down there! Try again later.'
          setState({
            ...state,
            formErrors: {
              ...defaultProps.formErrors,
              general: msg,
            },
          })
        } else if (error && error.response) {
          const msg = 'Please ensure the verification code is correct.'
          const formattedErrors = camelize(error.response.data)
          setState({
            ...state,
            formErrors: {
              ...defaultProps.formErrors,
              ...formattedErrors,
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
    currentForm = <VerificationForm submitValidation={validateCode} formErrors={state.formErrors} />
  } else if (state.verified) {
    currentForm = <SignUpSuccess />
  }

  return (
    <Fragment>
      <Container>
        <Grid textAlign="center" style={{ height: '95vh' }} verticalAlign="middle">
          <Grid.Column textAlign="left" style={{ maxWidth: 400 }}>
            <Header />
            {currentForm}
          </Grid.Column>
        </Grid>
        <Footer />
      </Container>
    </Fragment>
  )
}

export default FormContainer

/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React, { useEffect, useState } from 'react'
import { Segment, Form, Transition, Message } from 'semantic-ui-react'
import useSignUpForm from './hooks'
import { SignUpFormProps } from './types'

const SignUpForm = (props: SignUpFormProps) => {
  const [visibility, setVisiblity] = useState(false)

  const verifyDetails = () => {
    // eslint-disable-next-line no-use-before-define, @typescript-eslint/no-use-before-define
    props.submitDetails(formValues)
  }

  const { formValues, handleFormValues, handleSubmit } = useSignUpForm(verifyDetails)

  const { formErrors, loading } = props
  const nameErrors = formErrors.name ? { error: formErrors.name } : {}
  const phoneNumberErrors = formErrors.phoneNumber ? { error: formErrors.phoneNumber } : {}
  const postalCodeErrors = formErrors.postalCode ? { error: formErrors.postalCode } : {}

  useEffect(() => {
    setVisiblity(true)
  }, [])

  return (
    <Transition visible={visibility} animation="fade" duration={800}>
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
              placeholder="0421 222 333"
              name="phoneNumber"
              type="tel"
              required
              onChange={handleFormValues}
              value={formValues.phoneNumber}
              icon="phone"
              iconPosition="left"
            />
          </Form.Field>
          <Form.Field>
            <label style={{ color: 'white' }}>Postcode</label>
            <Form.Input
              {...postalCodeErrors}
              placeholder="3000"
              name="postalCode"
              type="text"
              required
              onChange={handleFormValues}
              value={formValues.postalCode}
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
            loading={loading}
          >
            Verify Number
          </Form.Button>
        </Segment>
      </Form>
    </Transition>
  )
}

export default SignUpForm

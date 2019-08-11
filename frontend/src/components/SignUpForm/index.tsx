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

  const { formErrors } = props
  const nameErrors = formErrors.name ? { error: formErrors.name } : {}
  const phoneNumberErrors = formErrors.phone_number ? { error: formErrors.phone_number } : {}
  const postalCodeErrors = formErrors.postcode ? { error: formErrors.postcode } : {}

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
              placeholder="3000"
              name="postcode"
              type="text"
              required
              onChange={handleFormValues}
              value={formValues.postcode}
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
    </Transition>
  )
}

export default SignUpForm

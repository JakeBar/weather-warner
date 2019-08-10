import React from 'react'
import { shallow } from 'enzyme'
import SignUpForm from '../index'

const mockProps = {
  formErrors: {
    general: '',
    name: '',
    phone_number: '',
    postal_code: '',
    verification_code: '',
  },
  submitDetails: (f: Function) => f,
}

describe('SignUpForm', () => {
  describe('component', () => {
    it('Renders simple component', () => {
      const wrapper = shallow(<SignUpForm {...mockProps} />)
      expect(wrapper.find('Form')).toHaveLength(1)
    })
  })
})

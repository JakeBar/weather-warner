import React from 'react'
import { shallow } from 'enzyme'
import VerificationForm from '../index'

const mockProps = {
  formErrors: {
    general: '',
    verificationCode: '',
  },
  phoneNumber: '0421999444',
  submitValidation: (f: Function) => f,
}

describe('VerificationForm', () => {
  describe('component', () => {
    it('Renders simple component', () => {
      const wrapper = shallow(<VerificationForm {...mockProps} />)
      expect(wrapper.find('Form')).toHaveLength(1)
    })
  })
})

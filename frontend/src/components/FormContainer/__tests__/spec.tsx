import React from 'react'
import { shallow } from 'enzyme'
import FormContainer from '../index'

describe('FormContainerPage', () => {
  describe('component', () => {
    it('Renders simple component', () => {
      const wrapper = shallow(<FormContainer />)
      expect(wrapper.find('Fragment')).toHaveLength(1)
    })
  })
})

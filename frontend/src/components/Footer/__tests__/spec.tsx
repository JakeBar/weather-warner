import React from 'react'
import { shallow } from 'enzyme'
import Footer from '../index'

describe('Footer', () => {
  describe('component', () => {
    it('Renders Footer component', () => {
      const wrapper = shallow(<Footer />)
      expect(wrapper.find('Segment')).toHaveLength(1)
    })
  })
})

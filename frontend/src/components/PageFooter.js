import React, { Component, Fragment } from 'react';
import { Popover, Button } from 'antd';

class PageFooter extends Component {
  state = {
    visible: false,
  };

  handleVisibleChange = visible => {
    this.setState({ visible });
  };

  aboutContent = (
    <Fragment>
      <p>
        <span className="site-title">
          <span className="slashes">//</span>moocmaven {''}
        </span>
         searches course from over tens of thousands courses from various moocs provider  We’re hoping to add more soon…
      </p>
      <p>
      It searches for the meaning keyword you enter.
      </p>
    </Fragment>
  );

  render() {
    return (
      <div className="page-footer">
        <div className="page-footer-items">
          <div className="page-footer-item">
            <Popover
              content={this.aboutContent}
              trigger="click"
              visible={this.state.visible}
              onVisibleChange={this.handleVisibleChange}
              overlayStyle={{ width: '400px' }}
              placement="top"
            >
              <Button type="link">
                About
              </Button>
            </Popover>
          </div>
            <div className="page-footer-item">
                <a href="https://api.moocmaven.com/docs">
                    API Docs
                </a>
            </div>
          <div className="page-footer-item">
            <a href="mailto:atatang@stu.kau.edu.sa">
              Contact
            </a>
          </div>
        </div>
      </div>
    );
  }
}

export default PageFooter;

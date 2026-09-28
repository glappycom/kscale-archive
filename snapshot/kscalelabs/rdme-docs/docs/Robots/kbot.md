---
title: K-Bot
excerpt: An overview of the K-Bot hardware
deprecated: false
hidden: false
metadata:
  robots: index
---
![](https://files.readme.io/d46d39701961f72ee8b71cea1518ce2cc56a6e4dfcbfca9014336ce113cc7594-image.png)

<br />

<Cards columns={3}>
  <Card title="K-Bot Monorepo" href="https://github.com/kscalelabs/kbot" icon="fa-home" target="_blank">
    The main repository where we collect everything related to K-Bot
  </Card>

  <Card title="K-OS" href="https://github.com/kscalelabs/kos-kbot" icon="fa-user">
    The K-OS backend for K-Bot
  </Card>

  <Card title="K-Sim" href="https://github.com/kscalelabs/ksim-kbot" icon="fa-star">
    Policy training and deployment code for K-Bot
  </Card>
</Cards>

## Motor ID Mapping

Motors each have their own unique CAN ID. We use a consistent naming convention to make development easier.

<Image align="center" src="https://files.readme.io/5ec636cbfb120627a32df54ed5a1d576c44894376a80735dfc1e7c4992435300-kbot.jpg" />
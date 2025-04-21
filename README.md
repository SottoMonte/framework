
  
    
  
  Koyeb Serverless Platform
  
    Deploy a Django application on Koyeb
    
    Learn more about Koyeb
    ·
    Explore the documentation
    ·
    Discover our tutorials
  



## About Koyeb and the Django example application

Koyeb is a developer-friendly serverless platform to deploy apps globally. No-ops, servers, or infrastructure management.
This repository contains a Django application you can deploy on the Koyeb serverless platform for testing.

This example application is designed to show how a Django application can be deployed on Koyeb.

## Getting Started

Follow the steps below to deploy and run the Django application on your Koyeb account.

### Requirements

You need a Koyeb account to successfully deploy and run this application. If you don't already have an account, you can sign-up for free [here](https://app.koyeb.com/auth/signup).

### Deploy using the Koyeb button

The fastest way to deploy the Django application is to click the **Deploy to Koyeb** button below.

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/koyeb/example-django&branch=main&name=django-on-koyeb&env[PORT]=8000&env[DJANGO_ALLOWED_HOSTS]=.koyeb.app&ports=8000;http;/)

Clicking on this button brings you to the Koyeb App creation page with everything pre-set to launch this application.

_To modify this application example, you will need to fork this repository. Checkout the [fork and deploy](#fork-and-deploy-to-koyeb) instructions._

### Fork and deploy to Koyeb

If you want to customize and enhance this application, you need to fork this repository.

If you used the **Deploy to Koyeb** button, you can simply link your service to your forked repository to be able to push changes.
Alternatively, you can manually create the application as described below.

On the [Koyeb Control Panel](https://app.koyeb.com/), on the **Overview** tab, click the **Create Web Service** button to begin.

1. Select **GitHub** as the deployment method.
2. In the repositories list, select the repository you just forked.
3. Towards the bottom, choose a name for your App, i.e. `django-on-koyeb`.
4. Expand the **Environment variables** section .  Click **Add variable** to create a `DJANGO_ALLOWED_HOSTS` variable set to `-.koyeb.app`, changing `` and `` to match your information.
5. Click **Deploy**.

You land on the deployment page where you can follow the build of your Django application. Once the build is completed, your application is being deployed and you will be able to access it via `-.koyeb.app`.

## Contributing
If you have any questions, ideas or suggestions regarding this application sample, feel free to open an [issue](//github.com/koyeb/example-django/issues) or fork this repository and open a [pull request](//github.com/koyeb/example-django/pulls).

## Contact

[Koyeb](https://www.koyeb.com) - [@gokoyeb](https://twitter.com/gokoyeb) - [Slack](http://slack.koyeb.com/)

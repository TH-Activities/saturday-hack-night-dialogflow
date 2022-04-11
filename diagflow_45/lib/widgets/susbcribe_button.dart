import 'package:flutter/material.dart';
import 'package:landingpage/utils/myColors.dart';
import 'package:landingpage/utils/strings.dart';
import 'package:landingpage/utils/responsive_widget.dart';

class SubscribeButton extends StatelessWidget {
  var emailImage = "assets/email.png";

  @override
  Widget build(BuildContext context) {
    return InkWell(
      child: Container(
        height: 40,
        decoration: BoxDecoration(
            gradient: LinearGradient(
                colors: [Theme.of(context).primaryColor, Theme.of(context).secondaryHeaderColor],
                begin: Alignment.bottomRight,
                end: Alignment.topLeft),
            borderRadius: BorderRadius.circular(20.0),
            boxShadow: [
              BoxShadow(
                  color: Theme.of(context).accentColor.withOpacity(.3),
                  offset: Offset(0, 8),
                  blurRadius: 8.0)
            ]),
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: () {}, //TODO
            child: Center(
              child: buildButton(context),
            ),
          ),
        ),
      ),
    );
  }


  Widget buildButton(BuildContext context) {
    if (ResponsiveWidget.isSmallScreen(context))
      return buildSmallButton(context);
    else
      return buildLargeButton(context);
  }

  Widget buildLargeButton(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Text(
          Strings.subscribeButton,
          style: TextStyle(
              color: MyColors.white1,
              fontSize: ResponsiveWidget.isSmallScreen(context)
                  ? 12
                  : ResponsiveWidget.isMediumScreen(context)
                  ? 12
                  : 16,
              letterSpacing: 1),
        ),
        SizedBox(
          width: ResponsiveWidget.isSmallScreen(context)
              ? 4
              : ResponsiveWidget.isMediumScreen(context) ? 6 : 8,
        ),
        Image.network(
          emailImage,
          color: MyColors.white1,
          width: ResponsiveWidget.isSmallScreen(context)
              ? 12
              : ResponsiveWidget.isMediumScreen(context) ? 12 : 20,
          height: ResponsiveWidget.isSmallScreen(context)
              ? 12
              : ResponsiveWidget.isMediumScreen(context) ? 12 : 20,
        )
      ],
    );
  }

  Widget buildSmallButton(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Image.asset(
          emailImage,
          color: MyColors.white1,
          width: ResponsiveWidget.isSmallScreen(context)
              ? 12
              : ResponsiveWidget.isMediumScreen(context) ? 12 : 20,
          height: ResponsiveWidget.isSmallScreen(context)
              ? 12
              : ResponsiveWidget.isMediumScreen(context) ? 12 : 20,
        )
      ],
    );
  }
}

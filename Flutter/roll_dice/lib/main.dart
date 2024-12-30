import 'package:flutter/material.dart';
import 'package:roll_dice/login/login.dart';

void main() {
  runApp(MaterialApp(
      title: 'Sesas',
      home: Scaffold(
          body: Container(
        decoration: BoxDecoration(
            gradient: LinearGradient(colors: [
          const Color.fromARGB(255, 26, 131, 250),
          const Color.fromARGB(255, 74, 158, 254),
        ], begin: Alignment.topCenter, end: Alignment.bottomCenter)),
        // alignment: Alignment.topCenter,
        child: Center(
          child: Login(),
        ),
      ))));
}

import 'package:flutter/material.dart';
import 'dart:math';

class AcessWidget extends StatefulWidget {
  const AcessWidget({super.key});

  @override
  State<AcessWidget> createState() {
    return _AcessWidget();
  }
}

class _AcessWidget extends State<AcessWidget> {
  String textChange = 'Sesas Num.: Null';
  var random = Random();

  void method() {
    int randomNum = random.nextInt(11);
    setState(() {
      textChange = 'Sesas Num.: $randomNum';
    });
  }

  @override
  Widget build(context) {
    return Column(children: [
      Text(
        textChange,
        style: TextStyle(fontSize: 40),
      ),
      TextButton.icon(
          onPressed: method,
          style: TextButton.styleFrom(
              padding: const EdgeInsets.only(top: 20),
              minimumSize: Size(40, 40)),
          icon: const Icon(Icons.import_contacts_sharp),
          label: const Text('Enviar')),
    ]);
  }
}

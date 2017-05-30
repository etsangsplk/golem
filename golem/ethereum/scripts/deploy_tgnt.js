var tgnt_init = "0x6060604052341561000c57fe5b5b6105608061001c6000396000f300606060405236156100725763ffffffff60e060020a60003504166306fdde03811461007457806318160ddd14610104578063313ce5671461012657806370a082311461014c57806395d89b411461017a578063a9059cbb1461020a578063efc81a8c1461023d578063fa369e661461024f575bfe5b341561007c57fe5b61008461026c565b6040805160208082528351818301528351919283929083019185019080838382156100ca575b8051825260208311156100ca57601f1990920191602091820191016100aa565b505050905090810190601f1680156100f65780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561010c57fe5b6101146102a3565b60408051918252519081900360200190f35b341561012e57fe5b6101366102a9565b6040805160ff9092168252519081900360200190f35b341561015457fe5b610114600160a060020a03600435166102ae565b60408051918252519081900360200190f35b341561018257fe5b6100846102cd565b6040805160208082528351818301528351919283929083019185019080838382156100ca575b8051825260208311156100ca57601f1990920191602091820191016100aa565b505050905090810190601f1680156100f65780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561021257fe5b610229600160a060020a0360043516602435610304565b604080519115158252519081900360200190f35b341561024557fe5b61024d6103af565b005b341561025757fe5b61024d600480356024810191013561043c565b005b60408051808201909152601881527f5465737420476f6c656d204e6574776f726b20546f6b656e0000000000000000602082015281565b60005481565b601281565b600160a060020a0381166000908152600160205260409020545b919050565b60408051808201909152600481527f74474e5400000000000000000000000000000000000000000000000000000000602082015281565b600160a060020a03331660009081526001602052604081205482811080159061032d5750600083115b156103a357600160a060020a0333811660008181526001602090815260408083209588900395869055938816808352918490208054880190558351878152935191937fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef929081900390910190a3600191506103a8565b600091505b5092915050565b600160a060020a033316600090815260016020526040902054683635c9adc5dea00000908190106103df57610000565b600160a060020a0333166000818152600160209081526040808320805486019055825485018355805185815290517fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef929181900390910190a35b50565b600160a060020a033316600090815260016020526040812054908080805b8584101561050f5786868581811061046e57fe5b60200291909101359350839250740100000000000000000000000000000000000000009050825b049050848111156104a557610000565b600160a060020a0380831660008181526001602090815260409182902080548601905581518581529151988590039892933316927fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef9281900390910190a35b83600101935061045a565b600160a060020a03331660009081526001602052604090208590555b505050505050505600a165627a7a72305820375e7b9a106acf43ec773e99f84ab5daa4ddfa7995ab6ea16851b56a93b4c5cf0029"

a = personal.listAccounts[0]
b = eth.getBalance(a, 'pending')
console.log("Balance: " + b)
tx = personal.sendTransaction({'from': a, 'data': tgnt_init, 'gas': 500000, 'gasPrice': 2000000000})
console.log("Deployment transaction: " + tx)